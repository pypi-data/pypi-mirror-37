import errno
import hashlib
import json
import os
import tempfile
import uuid


###############################################################################
##  Node store                                                               ##
###############################################################################
##
## TODO
##
## - regression tests
## - benchmarks
## - use slots where appropriate
## - cache attributes
## - cache nodes on tx
## - readonly tx
## - export node to json

class Backend(object):

    def __call__(self, schema = None, graph = None, read_only = True):
        if graph is None:
            graph = Graph
        if schema is None:
            schema = NoSchema()
        return graph(schema, self, read_only)

    def view(self, schema = None, graph = None):
        s = self(schema, graph)
        s.conn = self.connect(True)
        return s

    def connect(self, read_only):
        raise NotImplementedError
    def disconnect(self, conn, error):
        raise NotImplementedError

    # low-level backend managemets functions. XXX use a specific accessor?
    def version(self, schema = "base"):
        raise NotImplementedError
    def update(self, schema = "base", to = 100000):
        raise NotImplementedError
    def reset(self):
        raise NotImplementedError
    def drop(self):
        raise NotImplementedError
    def statistics(self, schema = "base", to = 100000):
        raise NotImplementedError

    # Content accessors
    def nodes(self, conn):
        raise NotImplementedError
    def attr(self, conn, key, lang):
        raise NotImplementedError
    def content(self, conn, key, lang):
        raise NotImplementedError
    def tagset(self, conn, key):
        raise NotImplementedError
    def link(self, conn, key):
        raise NotImplementedError

    # XXX experimetal
    def facet(self, conn, name):
        raise NotImplementedError


def backend(confstring):
    name, config = confstring.split("://", 1)
    if name == "sqlite":
        from . import udon_sqlite
        backend = udon_sqlite.SQLiteBackend(config)
    else:
        raise KeyError(name)
    return backend


class NoSchema(object):

    def getNodeClass(self, nodeTypeName):
        return Node

    def getClassAndType(self, classOrTypeName):
        if isinstance(classOrTypeName, str):
            return Node, classOrTypeName
        raise ValueError(classOrTypeName)

    def nodeFactory(self, graph, oid, type, klass = None):
        if not klass:
            klass = Node
        return klass(graph, oid)


class Schema(object):

    classes = None
    names = None

    def register(self, name):
        def _(klass):
            if not self.classes:
                self.classes = {}
            if not self.names:
                self.names = {}

            if klass in self.classes:
                raise KeyError(klass)
            if name in self.names:
                raise KeyError(klass)

            self.names[name] = klass
            self.classes[klass] = name
            return klass
        return _

    def getNodeClass(self, name):
        return self.names[name]

    def getClassAndType(self, classOrTypeName):
        if isinstance(classOrTypeName, str):
            return self.names[classOrTypeName], classOrTypeName
        return classOrTypeName, self.classes[classOrTypeName]

    def nodeFactory(self, graph, oid, type, klass = None):
        if not klass:
            klass = self.names[type]
        return klass(graph, oid)


class ReadOnly(Exception):
    pass


class Graph(object):

    conn = None

    def __init__(self, schema, backend, read_only):
        self.backend = backend
        self.schema = schema
        self.read_only = read_only

    def __enter__(self):
        assert self.conn is None
        self.conn = self.backend.connect(self.read_only)
        return self

    def __exit__(self, type, value, traceback):
        if (type, value, traceback) == (None, None, None):
            self.conn.commit()
            self.backend.disconnect(self.conn, False)
        else:
            self.conn.rollback()
            self.backend.disconnect(self.conn, True)
        del self.conn

    def list(self, type):
        klass, type = self.schema.getClassAndType(type)
        for oid in self.nodes.list(type):
            yield self.schema.nodeFactory(self, oid, type, klass)

    def all(self):
        for oid, type in self.nodes.all():
            yield self.schema.nodeFactory(self, oid, type)

    def node(self, oid, klass = None):
        if klass is Node:
            return Node(self, oid)
        if klass is not None:
            # ensure correctness
            return klass(self, oid)
        raw = Node(self, oid) # no cache!
        try:
            klass = self.schema.getNodeClass(raw.type)
        except TypeError:
            # For sqlite/udon:
            #
            #  File "/home/eric/app/essor/usr/lib/python3.6/site-packages/essor/udon.py", line 176, in node
            #   klass = self.schema.getNodeClass(raw.type)
            #  File "/home/eric/app/essor/usr/lib/python3.6/site-packages/essor/udon.py", line 401, in type
            #   return self.graph.nodes.type(self.oid)
            #  File "/home/eric/app/essor/usr/lib/python3.6/site-packages/essor/udon_sqlite.py", line 244, in type
            #   return c.fetchone()[0]
            #  TypeError: 'NoneType' object is not subscriptable
            raise KeyError(oid)
        return klass(self, oid)

    def new(self, classOrTypeName):
        if self.read_only:
            raise ReadOnly
        klass, type = self.schema.getClassAndType(classOrTypeName)
        oid = self.nodes.new(type)
        return self.schema.nodeFactory(self, oid, type, klass)

    @property
    def nodes(self):
        return self.backend.nodes(self.conn)
    def facet(self, name):
        return self.backend.facet(self.conn, name)
    def attr(self, key, lang):
        return self.backend.attr(self.conn, key, lang)
    def content(self, key, lang):
        return self.backend.content(self.conn, key, lang)
    def tagset(self, key):
        return self.backend.tagset(self.conn, key)
    def link(self, key):
        return self.backend.link(self.conn, key)


##
##  Facet : simple access to tables with oid key
##
class Facet(object):

    def __init__(self, conn, name):
        self.conn = conn
        self.name = name

    def insert(self, node, **kwargs):
        raise NotImplementedError
    def update(self, node, **kwargs):
        raise NotImplementedError
    def select(self, node, *cols):
        raise NotImplementedError

    def getColumn(self, node, col):
        return self.select(node, (col, ))[0]

    def setColumn(self, node, col, value):
        return self.update(node, **{ col: value }) 

##
## Accessors
##

class Accessor(object):

    @staticmethod
    def json_load(value):
        if value is None:
            return None
        return json.loads(value)

    @staticmethod
    def json_dump(value):
        if value is None:
            return None
        return json.dumps(value)

## Special accessor for node tables
class NodeAccessor(Accessor):

    def __init__(self, conn):
        self.conn = conn

    # XXX not wise
    #def __call__(self, *args):
    #    return self.list(*args)

    def generate_uuid(self):
        return str(uuid.uuid4())

    def all(self, type):
        raise NotImplementedError
    def list(self, type):
        raise NotImplementedError
    def new(self, type):
        raise NotImplementedError
    def uuid_to_oid(self, uuid):
        raise NotImplementedError
    def delete(self, node):
        raise NotImplementedError
    def uuid(self, node):
        raise NotImplementedError
    def type(self, node):
        raise NotImplementedError
    def ctime(self, node):
        raise NotImplementedError

class AttrAccessor(Accessor):

    def __init__(self, conn, key, lang):
        self.conn = conn
        self.key = key
        self.lang = lang

    def decode_text(self, value):
        assert isinstance(value, str)
        return value
    def decode_int(self, value):
        assert isinstance(value, int)
        return value
    def decode_float(self, value):
        assert isinstance(value, float)
        return value
    def decode_json(self, value):
        assert isinstance(value, str)
        return json.loads(value)
    def encode_text(self, value):
        assert isinstance(value, str)
        return value
    def encode_int(self, value):
        assert isinstance(value, int)
        return value
    def encode_float(self, value):
        assert isinstance(value, float)
        return value
    def encode_json(self, value):
        return json.dumps(value)

    def get(self, node, type = None): # XXX force_type = 'int'?
        raise NotImplementedError
    def set(self, node, value, type):
        raise NotImplementedError
    def unset(self, node):
        raise NotImplementedError
    def has(self, node):
        raise NotImplementedError
    def nodes(self, value = None, type = "text"):
        raise NotImplementedError

class ContentAccessor(Accessor):
    def __init__(self, conn, key, lang):
        self.conn = conn
        self.key = key
        self.lang = lang

    def content(self, node):
        raise NotImplementedError
    def store(self, node, content, mimetype, meta = None):
        raise NotImplementedError

class TagAccessor(Accessor):
    def __init__(self, conn, tagset):
        self.conn = conn
        self.tagset = tagset

    def tag(self, node, *tags):
        raise NotImplementedError
    def untag(self, node, *tags):
        raise NotImplementedError
    def tags(self, node):
        raise NotImplementedError
    def is_tagged(self, node, *tags):
        raise NotImplementedError

    def toggle_tags(self, node, *tags):
        if not tags:
            return
        untags = self.tags(node).intersection(set(tags))
        self.tag(node, *tags)
        self.untag(node, *untags)

class LinkAccessor(Accessor):
    def __init__(self, conn, key):
        self.conn = conn
        self.key = key

    def link(self, node, target, meta = None):
        raise NotImplementedError
    def unlink(self, node):
        raise NotImplementedError
    def target(self, node):
        raise NotImplementedError
    def sources(self, node):
        raise NotImplementedError

##
## XXX rework
##
class Property(object):
    def __init__(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)

class Content(Property):

    def open(self, store):
        return store.open(self.sha256)


class Link(Property):
    pass


def edit(method):
    def _(self, *args, **kwargs):
        if self.graph.read_only:
            raise ReadOnly
        return method(self, *args, **kwargs)
    return _

class Node(object):

    def __init__(self, graph, oid):
        self.graph = graph
        self.oid = oid

    ##
    ## Generic Node interface
    ##
    @edit
    def delete(self):
        return self.graph.nodes.delete(self.oid)
    @property
    def uuid(self):
        return self.graph.nodes.uuid(self.oid)
    @property
    def type(self):
        return self.graph.nodes.type(self.oid)
    @property
    def ctime(self):
        return self.graph.nodes.ctime(self.oid)

    ##
    ## Attributes
    ##

    _allowed_types = {
        "text": (str, ),
        "int": (int, ),
        "float": (float, ),
        "json": (str, int, float, dict, list)
    }
    _infer_type = {
        str: "text",
        int: "int",
        float: "float",
        dict: "json",
        list: "json"
    }
    def get(self, key, lang = '', type = None):
        return self.graph.attr(key, lang).get(self.oid, type = type)
    def has(self, key, lang = ''):
        return self.graph.attr(key, lang).has(self.oid)

    @edit
    def set(self, key, value, lang = '', _type = None):
        if _type is None:
            try:
                _type = self._infer_type[type(value)]
            except KeyError:
                raise TypeError(type(value))
        else:
            assert isinstance(value, *self._allowed_types[_type])
        return self.graph.attr(key, lang).set(self.oid, value, type = _type)

    @edit
    def unset(self, key, lang = ''):
        return self.graph.attr(key, lang).unset(self.oid)

    ##
    ##  Content storage
    ##
    def content(self, key, lang = ''):
        id, sha256, size, mimetype, mtime, meta = self.graph.content(key, lang).content(self.oid)
        if id is None:
            return None
        return Content(id = id, key = key, lang = lang, sha256 = sha256, mimetype = mimetype, size = size, mtime = mtime)

    @edit
    def store(self, store, key, data, mimetype, meta = None, lang = ''):
        size = len(data)
        sha256 = store.put(data)
        id, sha256, size, mimetype, mtime, meta = self.graph.content(key, lang).store(self.oid, sha256, size, mimetype, meta)
        return Content(id = id, key = key, lang = lang, sha256 = sha256, mimetype = mimetype, size = size, mtime = mtime)

    ##
    ##  Tags
    ##
    @edit
    def tag(self, tagset, *tags):
        return self.graph.tagset(tagset).tag(self.oid, *tags)
    @edit
    def untag(self, tagset, *tags):
        return self.graph.tagset(tagset).untag(self.oid, *tags)
    def tags(self, tagset):
        return self.graph.tagset(tagset).tags(self.oid)
    def isTagged(self, tagset, *tags):
        return self.graph.tagset(tagset).is_tagged(self.oid, *tags)
    @edit
    def toggleTags(self, tagset, *tags):
        return self.graph.tagset(tagset).toggle_tags(self.oid, *tags)

    ##
    ##  Links
    ##
    @edit
    def link(self, key, target, meta = None):
        if isinstance(target, Node):
            target = target.oid
        if not isinstance(target, int):
            raise TypeError("target must be a Node or an integer", target)
        return self.graph.link(key).link(self.oid, target, meta = meta)
    @edit
    def unlink(self, key):
        return self.graph.link(key).unlink(self.oid)
    def linkTarget(self, key):
        oid = self.graph.link(key).target(self.oid)
        if oid is not None:
            return self.graph.node(oid)
    def linkSources(self, key):
        return [ self.graph.node(oid) for oid in self.graph.link(key).sources(self.oid) ]
    def hasLink(self, key):
        return self.graph.link(key).has(self.oid)

    ##
    ## dump
    ##
    def asJSON(self):
        return  { "oid": self.oid,
                  "type": self.type,
                  "uuid": self.uuid,
                  "ctime": self.ctime,
                  "attrs": [ { "key": key, "lang": lang, "value": self.get(key, lang = lang) }
                             for (key, lang) in self.graph.nodes.attributes(self.oid) ],
                  "contents" : [ { "key": c.key, "lang": c.lang, "mtime": c.mtime, "size": c.size, "sha256" : c.sha256, "mimetype": c.mimetype }
                                 for c in self.graph.nodes.contents(self.oid) ],
                  "tags" : [  { "tagset": key, "tags": sorted(self.tags(key)) }
                              for key in self.graph.nodes.tagsets(self.oid) ],
                  "links": [ { "key": link.key, "target": link.target, "meta": link.meta }
                             for link in self.graph.nodes.links(self.oid) ]
              }
