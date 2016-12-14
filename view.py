

import os
import urllib
import json
import webapp2
import jinja2
from google.appengine.api import memcache


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "template")),
    extensions=['jinja2.ext.autoescape'])


class ElBase:
    pass




class ElPage(ElBase):
    def __init__(self):
        self.title = ''
        self.content = ''
        self.loggedin = False

        nav = ElNav('bdotymainnav')
        self.menu = nav.render()


    def render(self):
        template = JINJA_ENVIRONMENT.get_template('page.html')
        return template.render(vars(self))


class ElList(ElBase):

    def __init__(self):
        self.items = []

    def add(self, text, link):
        self.items.append({'text': text, 'link': link})

    def render(self):
        template = JINJA_ENVIRONMENT.get_template('list.html')
        return template.render(vars(self))


class ElNav(ElBase):
    def __init__(self, navname):
        cache = memcache.get(navname)
        self.cached = False

        if cache is not None:
            self.cached = True
            self.html = cache
        else:
            with open('nav.json') as nav_file:    
                self.nav = json.load(nav_file)

    def render(self):
        if self.cached:
            return self.html
        else:
            template = JINJA_ENVIRONMENT.get_template('nav.html')
            return template.render(vars(self))
