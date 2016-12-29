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
from google.appengine.api import memcache, users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

import models
import view


class BaseHandler(webapp2.RequestHandler):
    def __init__(self, request, response):
        self.initialize(request, response)

        self.user = users.get_current_user()
        self.loggedin = bool(self.user)


    # def handle_exception(self, exception, debug):
    #     # Log the error.
    #     logging.exception(exception)

    #     # Set a custom message.
    #     response.write('An error occurred.')

    #     # If the exception is a HTTPException, use its error code.
    #     # Otherwise use a generic 500 error code.
    #     if isinstance(exception, webapp2.HTTPException):
    #         response.set_status(exception.code)
    #     else:
    #         response.set_status(500)




class MainHandler(BaseHandler):
    def get(self):
        p = view.ElPage(self.user, self.request.path)
        p.title = ''
        p.content = '<p>Hello, World!</p>'
        p.navactive = 'home'

        self.response.write(p.render())


class HymnListHandler(BaseHandler):
    def get(self):
        p = view.ElHymnListPage(self.user)
        p.title = 'Hymn Book'
        p.hymn_q = models.Hymn.list()
        
        self.response.write(p.render())



class HymnHandler(BaseHandler):
    def get(self):
        k = self.request.get('k')
        try:
            h = ndb.Key(urlsafe=k).get()
        except:
            self.response.set_status(400)
            return

        p = view.ElHymnPage(h, self.user)

        self.response.write(p.render())


class EditHymnHandler(BaseHandler):
    def get(self):

        if not self.loggedin:
            self.response.set_status(403)
            return

        k = self.request.get('k')
        try:
            h = ndb.Key(urlsafe=k).get()
        except:
            self.response.set_status(400)
            return

        p = view.ElPage(self.user)
        p.title = 'Edit Hymn'
        p.navactive = 'hymns'

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
            return

        h.title = self.request.get('title')
        h.text = self.request.get('text')
        h.tags = self.request.get('tags')
        h.put()



class AddHymnHandler(BaseHandler):
    def get(self):
        if not self.loggedin:
            self.response.set_status(403)
            return

        p = view.ElPage(self.user, '/hymns/add')

        p.title = 'Add Hymn'
        p.navactive = 'hymns'

        f = view.ElForm()
        f.action = "/hymns/add"
        f.add(view.ElFormElem('input', 'title', 'Title: ', ''))
        f.add(view.ElFormElem('textarea', 'text', 'Text: ', ''))
        f.add(view.ElFormElem('input', 'tags', 'Tags: ', ''))
        f.add(view.ElFormElem('number', 'index', 'Index: ', ''))

        p.content = f.render()

        self.response.write(p.render())

    def post(self):
        if not self.loggedin:
            self.response.set_status(403)
            return
            
        h = models.Hymn.create()
        h.title = self.request.get('title')
        h.text = self.request.get('text')
        h.tags = self.request.get('tags')
        h.index = int(self.request.get('index'))
        h.put()






class TeamListHandler(BaseHandler):
    def get(self):
        p = view.ElTeamListPage(self.user)

        t_q = models.Team.list()
        p.team_q = t_q.fetch(10)

        self.response.write(p.render())


class TeamHandler(BaseHandler):
    def get(self):
        k = self.request.get('t')
        try:
            t = ndb.Key(urlsafe=k).get()
        except:
            self.response.set_status(400)
            return

        p = view.ElTeamPage(t, self.user)

        p.players = models.Player.list(t, 0)
        
        self.response.write(p.render())



class ProfileHandler(BaseHandler):
    def get(self):
        k = self.request.get('p')
        try:
            h = ndb.Key(urlsafe=k).get()
        except:
            self.response.set_status(400)
            return

        p = view.ElProfilePage(h, self.user)

        self.response.write(p.render())



class TeamEditHandler(BaseHandler):
    def get(self):
        k = self.request.get('t')
        try:
            t = ndb.Key(urlsafe=k).get()
        except:
            self.error(400)
            return

        p = view.ElPage(self.user, '/team/edit?t'+k)
        p.navactive = 'profiles'
        p.title = "Edit Team"

        f = view.ElForm()
        f.action = '/team/edit'

        f.add(view.ElFormElem('hidden', 't', '', k))
        f.add(view.ElFormElem('input', 'name', 'Name', t.name))
        f.add(view.ElFormElem('textarea', 'summary', 'Summary', t.summary))

        p.content = f.render()
        self.response.write(p.render())

    def post(self):
        k = self.request.get('t')
        try:
            t = ndb.Key(urlsafe=k).get()
        except:
            self.error(400)
            return

        t.summary = self.request.get('summary')
        t.name = self.request.get('name')

        t.put()

        self.response.redirect('/team?t=' + t)

class TeamSetImageFormHandler(BaseHandler):
    def get(self):
        k = self.request.get('t')
        try:
            t = ndb.Key(urlsafe=k).get()
        except:
            self.error(400)
            return

        p = view.ElPage(self.user, '/team/editpic?t' + k)
        p.navactive = 'profiles'
        p.title = 'Edit Team Image'

        f = view.ElForm()
        f.action = blobstore.create_upload_url('/team/editpic')

        f.add(view.ElFormElem('hidden', 't', '', k))
        f.add(view.ElFormElem('image', 'picture', 'Picture', ''))
        p.content = f.render()

        self.response.write(p.render())


class TeamSetImageHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        k = self.request.get('t')
        try:
            t = ndb.Key(urlsafe=k).get()
        except:
            self.error(400)

        try:
            upload = self.get_uploads()[0]

            t.picture = upload.key
            t.put()

            self.redirect('/team?t=' + t)

        except:
            self.error(500)



class ImageHandler(blobstore_handlers.BlobstoreDownloadHandler):
    @staticmethod
    def url(img):
        return '/res/' + img.key + ".png"

    def get(self, img):
        if not blobstore.get(img):
            self.error(404)
        else:
            self.send_blob(img)




class InitHandler(BaseHandler):
    def get(self):
        models.setting.set("currentyear", "2s3s_17")
        yr = models.year.create("2s3s_17")

        for tn in ["Wanderers", "Nomads", "Squanderers", "Bedouin"]:
            t = models.Team(parent=yr.key)
            t.year = 2017
            t.name = tn
            t.put()







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
    ('/teams', TeamListHandler),
    ('/team/edit', TeamEditHandler),
    ('/team/edit/submit', TeamEditSubmitHandler),
    ('/team/editpic', TeamSetImageFormHandler),
    ('/team/editpic/submit', TeamSetImageHandler),
    ('/team', TeamHandler),
    ('/profile', ProfileHandler),
    ('/init', InitHandler),
    ('/res/([^\.]+)?\.png', ImageHandler),
    ('/', MainHandler)
], debug=True)
