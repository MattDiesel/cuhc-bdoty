

from google.appengine.ext import ndb

import json




class Hymn(ndb.Model):
    """Hymn Entity"""
    title = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    text = ndb.TextProperty()
    tags = ndb.StringProperty()
    index = ndb.IntegerProperty()


    @classmethod
    def common_ancestor(cls):
        return ndb.Key("book", "cuhc")

    @classmethod
    def create(cls):
        h = cls(parent=cls.common_ancestor())
        return h

    @classmethod
    def list(cls):
        return cls.query(ancestor=cls.common_ancestor(), projection=['title', 'tags']).order(cls.index, -cls.created)

    class HymnEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Hymn):
                return {'title': obj.title, 'text': obj.text}

            return json.JSONEncoder.default(self, obj)

    class QueryEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, ndb.Query):
                ret = []
                for h in obj.fetch(200):
                    ret.append([h.key.urlsafe(), h.title])
                return ret

            return json.JSONEncoder.default(self, obj)




class Team(ndb.Model):
    year = ndb.IntegerProperty()
    index = ndb.IntegerProperty()
    name = ndb.StringProperty()

    summary = ndb.TextProperty()

class Player(ndb.Model):
    """A CUHC Member"""

    name = ndb.StringProperty()
    team = ndb.KeyProperty(kind=Team)

    profile = ndb.TextProperty()


