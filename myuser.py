from google.appengine.ext import ndb
from mylist import MyList

class MyUser(ndb.Model):
    my_list = ndb.KeyProperty(kind=MyList, repeated=True)
