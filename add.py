from google.appengine.ext import ndb
import webapp2
import renderer
import utilities
import os
import jinja2
from mylist import MyList

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Add(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template_values = {
                'user': utilities.get_user(),
                'my_list': utilities.getanagrams_from_user(utilities.getuser())
                }
        template = JINJA_ENVIRONMENT.get_template('add.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        if self.request.get('cancel') == 'Cancel':
            return self.redirect("/")

        my_user = utilities.getuser()
        input_text = utilities.preparetextinput(self.request.get('value'))
        self.add(input_text, my_user)

    def add(self, text, my_user):
        permutations = utilities.permutations(text)
        words = utilities.filterenglishwords(permutations)
        if text is not None or text != '':

            anagram_id = my_user.key.id() + '/' + utilities.generateid_for_users(text)
            anagram_key = ndb.Key(MyList, anagram_id)
            my_list = anagram_key.get()

            if my_list:
                utilities.addtoanagram(text, words, anagram_key)
            else:
                utilities.addanagram_new(my_user, text, words, anagram_id, anagram_key)
        self.redirect("/")
