

import os
import urllib
import json
import webapp2
import jinja2
from google.appengine.api import memcache, users


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "template")),
    extensions=['jinja2.ext.autoescape'])


class ElBase(object):
    def __init__(self, tmp):
        self.template = tmp

    def render(self):
        template = JINJA_ENVIRONMENT.get_template(self.template + '.html')
        return template.render(vars(self))





class ElPage(ElBase):
    def __init__(self, user, url='/', tmp='page'):
        super(ElPage, self).__init__(tmp)

        self.title = ''
        self.content = ''
        self.url = url
        self.loggedin = bool(user)
        self.user = user

        self.loginurl = users.create_login_url('/') # TODO: redirect to same page
        self.logouturl = users.create_logout_url('/')

        self.menu = ElCachedNav('bdoty-navmenu')

        if self.loggedin:
            self.usermenu = ElNav('bdoty-usermenu')
            self.usermenu.pos('right')

            self.usermenu.add(user)
            self.usermenu.addsep()
            self.usermenu.add('Logout', self.logouturl)
        else:
            self.loginmenu = ElNav('bdoty-loginmenu')
            self.loginmenu.pos('right')
            self.loginmenu.add('Login', self.loginurl)


class ElHymnPage(ElPage):
    def __init__(self, hymn, user):
        super(ElHymnPage, self).__init__(user, '/hymn?k=' + hymn.key.urlsafe(), 'hymn')

        self.navactive = 'hymns'
        self.title = hymn.title
        self.text = hymn.text
        self.hkey = hymn.key.urlsafe()


class ElHymnListPage(ElPage):
    def __init__(self, user):
        super(ElHymnListPage, self).__init__(user, '/hymns', 'hymnlist')

        self.navactive = 'hymns'
        self.title = 'Hymn Book'


class ElProfilePage(ElPage):
    def __init__(self, profile, user):
        super(ElProfilePage, self).__init__(user, '/profile?p=' + profile.key.urlsafe(), 'profile')

        self.navactive = 'profiles'
        self.title = profile.title
        self.text = profile.text
        self.hkey = profile.key.urlsafe()


class ElTeamPage(ElPage):
    def __init__(self, team, user):
        super(ElTeamPage, self).__init__(user, '/team?t=' + team.key.urlsafe(), 'team')

        self.navactive = 'profiles'
        self.title = team.name
        self.summary = team.summary
        self.team = team

        self.players = []

class ElTeamListPage(ElPage):
    def __init__(self, user):
        super(ElTeamListPage, self).__init__(user, '/teams', 'teamlist')

        self.navactive = 'profiles'
        self.title = 'Teams'

        self.team_q = []




class ElPanel(ElBase):
    def __init__(self, nm):
        super(ElPanel, self).__init__('panel')
        self.name = nm
        self.content = ''


class ElPopup(ElBase):
    def __init__(self, nm):
        super(ElPopup, self).__init__('popup')
        self.name = nm
        self.content = ''



class ElForm(ElBase):
    def __init__(self):
        super(ElForm, self).__init__('form')
        self.action = '.'
        self.method = 'POST'
        self.elements = []

    def add(self, elem):
        self.elements.append(elem)



class ElFormElem(ElBase):
    def __init__(self, typ, nm, lbl, val):
        super(ElFormElem, self).__init__('form_' + typ)
        self.type = typ
        self.label = lbl
        self.name = nm
        self.value = val


class ElList(ElBase):

    def __init__(self):
        super(ElList, self).__init__('list')
        self.items = []
        self.filterable = 'false'
        self.listtype = 'ul'

        self.splitlink = ''
        self.splitlinklink = ''
        self.splitlinktext = ''

    def add(self, text, link, icon=''):
        self.items.append({'text': text, 'link': link, 'icon': icon})


class ElNav(ElBase):
    def __init__(self, navname):
        super(ElNav, self).__init__('nav')
        self.name = navname
        self.cached = False

        self.nav = {'pos': 'left', 'submenu': []}

    def add(self, text, link=None, icon=None):
        self.nav['submenu'].append({'text': text, 'link': link, 'icon': icon})

    def addsep(self):
        self.nav['submenu'].append({'text': '', 'divider': 'True'})

    def pos(self, side):
        self.nav['pos'] = side


class ElCachedNav(ElNav):
    def __init__(self, navname):
        super(ElCachedNav, self).__init__(navname)

        cache = memcache.get(navname)
        self.cached = False

        if cache is not None:
            self.cached = True
            self.html = cache
        else:
            with open(navname + '.json') as nav_file:    
                self.nav = json.load(nav_file)

    def render(self):
        if self.cached:
            return self.html
        else:
            ret = super(ElCachedNav, self).render()

            # Add to memcache

            return ret
