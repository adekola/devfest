__author__ = 'adekola'
from to_do_model import ToDo
from google.appengine.ext import ndb

def addToDo(user, _title, _text):
    todo = ToDo(user_id=user, title=_title, text=_text)
    key = todo.put()
    id = str(key.id())
    new_to_do = {"user_id": user, "title": _title, "text": _text, "to_do_id": id}
    return new_to_do


def viewToDos(user_id):
    #get them ...filter by user id
    #query = ndb.gql('SELECT * FROM ToDo WHERE user_id = :1', user_id)
    query = ToDo.query(ToDo.user_id == user_id)
    to_do_dict = {"user_id": user_id}
    to_dos = list()
    for td in query:
        todo_item = {"title": td.title, "text": td.text, "to_do_id": td.key.id()}
        to_dos.append(todo_item)

    to_do_dict["to_dos"] = to_dos
    to_do_dict["to_do_count"] = len(to_dos)

    return to_do_dict


def viewAllToDos():
    query = ToDo.query()
    to_do_dict = dict()
    to_dos = list()
    for td in query:
        todo_item = {"title": td.title, "text": td.text, "to_do_id": td.key.id(), "user_id": td.user_id}
        to_dos.append(todo_item)

    to_do_dict["to_dos"] = to_dos
    to_do_dict["to_do_count"] = len(to_dos)

    return to_do_dict


def deleteToDo(user, to_do_id):
    #get them ..filter by user id
    to_do = ToDo.query(ToDo.user_id == user, ToDo.key.id() == to_do_id).fetch()
    result = to_do.delete()
    if result == None:
        return True
    else:
        return False
    #pick out the one by ID
    #delete it mehn
