

import os
import urllib
import json
import webapp2
import jinja2
from google.appengine.api import memcache


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "template")),
    extensions=['jinja2.ext.autoescape'])


class ElBase(object):
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

class ElHymnPage(ElPage):
    def __init__(self, hymn):
        super(ElHymnPage, self).__init__()

        self.navactive = 'hymns'
        self.title = hymn.title
        self.text = hymn.text
        self.hkey = hymn.key.urlsafe()

    def render(self):
        template = JINJA_ENVIRONMENT.get_template('hymn.html')
        return template.render(vars(self))

class ElHymnListPage(ElPage):
    def __init__(self):
        super(ElHymnListPage, self).__init__()

        self.navactive = 'hymns'
        self.title = 'Hymn Book'

    def render(self):
        template = JINJA_ENVIRONMENT.get_template('hymnlist.html')
        return template.render(vars(self))




class ElPanel(ElBase):
    def __init__(self, nm):
        self.name = nm
        self.content = ''

    def render(self):
        template = JINJA_ENVIRONMENT.get_template('panel.html')
        return template.render(vars(self))

class ElPopup(ElBase):
    def __init__(self, nm):
        self.name = nm
        self.content = ''

    def render(self):
        template = JINJA_ENVIRONMENT.get_template('popup.html')
        return template.render(vars(self))




class ElForm(ElBase):
    def __init__(self):
        self.action = '.'
        self.method = 'POST'
        self.elements = []

    def add(self, elem):
        self.elements.append(elem)

    def render(self):
        template = JINJA_ENVIRONMENT.get_template('form.html')
        return template.render(vars(self))


class ElFormElem(ElBase):
    def __init__(self, typ, nm, lbl, val):
        self.type = typ
        self.label = lbl
        self.name = nm
        self.value = val

    def render(self):
        template = JINJA_ENVIRONMENT.get_template('form_' + self.type + '.html')
        return template.render(vars(self))


class ElList(ElBase):

    def __init__(self):
        self.items = []
        self.filterable = 'false'
        self.listtype = 'ul'

        self.splitlink = ''
        self.splitlinklink = ''
        self.splitlinktext = ''

    def add(self, text, link, icon=''):
        self.items.append({'text': text, 'link': link, 'icon': icon})

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
