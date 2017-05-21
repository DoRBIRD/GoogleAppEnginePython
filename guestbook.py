import os
import urllib

import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'


def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity.
    We use guestbook_name as the key.
    """
    return ndb.Key('Guestbook', guestbook_name)


# [START greeting]
class Author(ndb.Model):
    """Sub model for representing an author."""
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)


class Greeting(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    author = ndb.StructuredProperty(Author)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)


# [END greeting]

# [START main_page]
class MainPage(webapp2.RequestHandler):
    def get(self):
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('templates/guestbook.html')
        self.response.write(template.render(template_values))


# [END main_page]

# [START guestbook]
class Guestbook(webapp2.RequestHandler):
    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each
        # Greeting is in the same entity group. Queries across the
        # single entity group will be consistent. However, the write
        # rate to a single entity group should be limited to
        # ~1/second.
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = Author(
                identity=users.get_current_user().user_id(),
                email=users.get_current_user().email())

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))


# [END guestbook]

# [START bootstrap_test]
class Bootstrap(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/bootstraptest.html')
        self.response.write(template.render())


# [END bootstrap_test]

# [START memory]
class Memory(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/memory.html')
        self.response.write(template.render())


# [END memory]


# [START Mockup]
class Animation():
    def __init__(self, user, title, date, file_id):
        self.user = user
        self.title = title
        self.date = date
        self.file_id = file_id


class Mockup(webapp2.RequestHandler):
    def get(self):
        user = "jonas"
        animations = [Animation("jonas", "My First Animation", "Yesterday", "0"),
                      Animation("jonas", "My Second Animation", "Today", "1")]
        template_values = {
            'user': user,
            'animations': animations,
        }
        template = JINJA_ENVIRONMENT.get_template('templates/mockupchild.html')
        self.response.write(template.render(template_values))


class MockupRender(webapp2.RequestHandler):
    def get(self, animation_id):
        user = "Jonas"
        template_values = {
            'user': user,
            'animation_id': animation_id,
        }
        template = JINJA_ENVIRONMENT.get_template('templates/mockupchildrender.html')
        self.response.write(template.render(template_values))



# [END Mockup]

# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook),
    ('/bootstrap_test', Bootstrap),
    ('/memory', Memory),
    ('/mockup', Mockup),
    ('/mockup_render_(\d+)', MockupRender),
], debug=True)
# [END app]
