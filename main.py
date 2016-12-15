#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import json
from StringIO import StringIO
import os
import urllib

import webapp2
import jinja2
from google.appengine.ext import ndb

import models
import view



class MainHandler(webapp2.RequestHandler):
    def get(self):
        p = view.ElPage()
        p.title = ''
        p.content = '<p>Hello, World!</p>'
        p.navactive = 'home'

        p.loggedin = False;

        
        self.response.write(p.render())


class HymnListHandler(webapp2.RequestHandler):
    def get(self):
        p = view.ElHymnListPage()
        p.title = 'Hymn Book'

        p.loggedin = True;
        p.hymn_q = models.Hymn.list()
        
        self.response.write(p.render())



class HymnHandler(webapp2.RequestHandler):
    def get(self):
        k = self.request.get('k')
        try:
            h = ndb.Key(urlsafe=k).get()
        except:
            self.response.set_status(400)

        p = view.ElHymnPage(h)
        p.loggedin = True

        self.response.write(p.render())

class EditHymnHandler(webapp2.RequestHandler):
    def get(self):

        k = self.request.get('k')
        try:
            h = ndb.Key(urlsafe=k).get()
        except:
            self.response.set_status(400)

        p = view.ElPage()
        p.title = 'Edit Hymn'

        f = view.ElForm()
        f.action = "/hymns/edit?k=" + k
        f.add(view.ElFormElem('input', 'title', 'Title: ', h.title))
        f.add(view.ElFormElem('textarea', 'text', 'Text: ', h.text))
        f.add(view.ElFormElem('input', 'tags', 'Tags: ', h.tags))

        p.content = f.render()

        self.response.write(p.render())

    def post(self):

        k = self.request.get('k')
        try:
            h = ndb.Key(urlsafe=k).get()
        except:
            self.response.set_status(400)

        h.title = self.request.get('title')
        h.text = self.request.get('text')
        h.tags = self.request.get('tags')
        h.put()



class AddHymnHandler(webapp2.RequestHandler):
    def get(self):
        p = view.ElPage()
        p.title = 'Add Hymn'
        p.loggedin = True

        f = view.ElForm()
        f.action = "/hymns/add"
        f.add(view.ElFormElem('input', 'title', 'Title: ', ''))
        f.add(view.ElFormElem('textarea', 'text', 'Text: ', ''))
        f.add(view.ElFormElem('input', 'tags', 'Tags: ', ''))
        f.add(view.ElFormElem('number', 'index', 'Index: ', ''))

        p.content = f.render()

        self.response.write(p.render())

    def post(self):
        h = models.Hymn.create()
        h.title = self.request.get('title')
        h.text = self.request.get('text')
        h.tags = self.request.get('tags')
        h.index = int(self.request.get('index'))
        h.put()







# class HymnRequest(webapp2.RequestHandler):
#     def get(self):
#         k = self.request.get('k')

#         try:
#             h = ndb.Key(urlsafe=k).get()

#             io = StringIO()
#             json.dump(h, io, cls=models.Hymn.HymnEncoder)

#             self.response.write(io.getvalue())
#         except:
#             self.response.set_status(400)


# class HymnListRequest(webapp2.RequestHandler):
#     def get(self):
#         hymns = models.Hymn.list()

#         io = StringIO()
#         json.dump(hymns, io, cls=models.Hymn.QueryEncoder)

#         self.response.write(io.getvalue())




app = webapp2.WSGIApplication([
    ('/hymns/add', AddHymnHandler),
    ('/hymns/edit', EditHymnHandler),
    ('/hymns/delete', EditHymnHandler),
    ('/hymns', HymnListHandler),
    ('/hymn', HymnHandler),
    ('/', MainHandler)
], debug=True)
