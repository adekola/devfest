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

import webapp2
import json
import crud
import os
import webapp2
import cgi
from google.appengine.api import users
from google.appengine.ext.webapp import template
from util.sessions import Session


session = Session() #global session object...works like magic


class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            user_data = {"user_id": user.user_id(), "name": user.nickname(), "logout_url": users.create_logout_url('/')}
            render(self, "index.html", user_data)
        else:
            login_url=users.create_login_url('/ViewToDos')
            data = {"login_url": login_url}
            render(self, "index.html", data)



class ViewToDos(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            user_data = {"user_id": user.user_id(), "name": user.nickname(), "logout_url": users.create_logout_url('/')}
            render(self, "view_to_dos.html", user_data)
        else:
            login_url=users.create_login_url('/ViewToDos')
            data = {"login_url": login_url}
            render(self, "view_to_dos.html", data)


#define classes for yur different API endpoints
class saveToDo(webapp2.RequestHandler):
    def post(self):
        request = self.request.body
        #extract the post body then return
        data = json.loads(request)
        user_id = data['user_id']
        title = data['title']
        text = data['text']
        result = crud.addToDo(user_id, title, text)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(result))


    def get(self):
        self.response.write('False')


class getToDosForUser(webapp2.RequestHandler):
    def get(self):
        user_id = self.request.get('user_id')
        to_dos = crud.viewToDos(user_id)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(to_dos))


    def post(self):
        self.response.write('False')


class getToDos(webapp2.RequestHandler):
    def get(self):
        to_dos = crud.viewAllToDos()
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(to_dos))

    def post(self):
        self.response.write('False')


class deleteToDo(webapp2.RequestHandler):
    def get(self):
        to_do_id = int(self.request.get('to_do_id'))
        user_id = int(self.request.get('user_id'))
        response = crud.deleteToDo(user_id, to_do_id)
        self.response.write(json.dump(response))

    def post(self):
        self.response.write('False')


def render(handler, template_file = "index.html", data={}):
    temp = os.path.join(
    os.path.dirname(__file__),
    'templates/' + template_file)
    if not os.path.isfile(temp):
        return False

    # Make a copy of the dictionary and add the path and session
    newval = dict(data)
    newval['path'] = handler.request.path
    handler.session = session

#love this part
    outStr = template.render(temp, data)
    handler.response.out.write(unicode(outStr))
    return True
app = webapp2.WSGIApplication([
    ('/', MainHandler),('/saveToDo', saveToDo), ('/getToDos', getToDos), ('/deleteToDo', deleteToDo),
    ('/getToDosForUser', getToDosForUser), ('/ViewToDos', ViewToDos)
], debug=True)
