from google.appengine.ext import ndb


class ToDo(ndb.Model):
    user_id = ndb.StringProperty()
    title = ndb.StringProperty()
    text = ndb.TextProperty()
    timeAdded = ndb.DateTimeProperty(auto_now_add=True)