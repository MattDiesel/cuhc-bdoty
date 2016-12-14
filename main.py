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

        p.loggedin = False;

        
        self.response.write(p.render())


class HymnListHandler(webapp2.RequestHandler):
    def get(self):
        p = view.ElPage()
        p.title = 'Hymn Book'
        p.content = '<p>Hello, World!</p>'

        p.loggedin = True;

        l = view.ElList()

        for i in range(1,10):
            l.add("Hello", "#")

        p.content += l.render()
        
        self.response.write(p.render())


class AddHymn(webapp2.RequestHandler):
    def get(self):
        models.Hymn.create("Wings of a Sparrow", "If I had the Wings of a Sparrow")
        self.response.write('Hello world!')







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
    ('/add', AddHymn),
    ('/hymns', HymnListHandler),
    ('/', MainHandler)
], debug=True)
