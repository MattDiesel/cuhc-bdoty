

from google.appengine.ext import ndb

import json
from datetime import datetime, timedelta



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
    name = ndb.StringProperty()

    summary = ndb.TextProperty()
    picture = ndb.BlobKeyProperty()

    @classmethod
    def common_ancestor(cls, year=0):
        if year == 0:
            year = setting.get("currentyear")

        return ndb.Key("year", year)

    @classmethod
    def create(cls, year=0):
        h = cls(parent=cls.common_ancestor(year))
        return h

    @classmethod
    def list(cls, year=0):
        return cls.query(ancestor=cls.common_ancestor(year), projection=['name', 'picture'])


class Player(ndb.Model):
    """A CUHC Member"""

    name = ndb.StringProperty()
    team = ndb.KeyProperty(kind=Team)
    shirt = ndb.IntegerProperty()
    index = ndb.IntegerProperty()

    profile = ndb.TextProperty()
    picture = ndb.BlobKeyProperty()

    @classmethod
    def common_ancestor(cls, year=0):
        if year == 0:
            year = setting.get("currentyear")

        return ndb.Key("year", year)

    @classmethod
    def create(cls, year=0):
        h = cls(parent=cls.common_ancestor(year))
        return h

    @classmethod
    def list(cls, tm, year=0):
        return cls.query(ancestor=cls.common_ancestor(year), projection=['name', 'picture']) \
            .filter(cls.team == tm.key) \
            .order(cls.index)


class year(ndb.Model):

    @classmethod
    def create(cls, yr):
        return cls.get_or_insert(yr)

class setting(ndb.Model):
    value = ndb.StringProperty()

    _timeout = timedelta(minutes=5)
    _local = {}
    _age = {}

    @classmethod
    def get(cls, sett):
        if sett not in cls._local or cls._age[sett]+cls._timeout < datetime.now():
            ret = cls.get_or_insert(sett).value
            cls._local[sett] = ret
            cls._age[sett] = datetime.now()
            return ret
        return cls._local[sett]

    @classmethod
    def set(cls, sett, value):
        k = cls.get_or_insert(sett)
        k.value = value
        k.put()
        cls._local[sett] = value
        cls._age[sett] = datetime.now()


    @classmethod
    def listkeys(cls):
        q = cls.query(keys_only=True).fetch(100)
        return q
        
