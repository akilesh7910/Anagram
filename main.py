from google.appengine.ext import ndb
import webapp2
import renderer
import utilities
from mylist import MyList
from add import Add

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        if utilities.user_loggedin():
            if not utilities.existing_user():
                utilities.addnewuser(utilities.get_user())
            result, word_Count, total_Count = utilities.getanagrams_from_user(utilities.getuser())
            renderer.render_main(self, utilities.getlogouturl(self), result, word_Count, total_Count)
        else:
            renderer.render_login(self, utilities.getloginurl(self))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        my_user = utilities.getuser()
        button = self.request.get('button')
        input_text = utilities.preparetextinput(self.request.get('value'))
        file = self.request.get('uploadFile')

        if button == 'Upload':
            openFile = open(file)
            readLine = openFile.readline()
            while readLine:
                word = (readLine.strip('\n\r')).lower()

                permutations = utilities.a_permutations(word)
                wordsinfo = utilities.filterenglishwords(permutations)

                anagram_id = my_user.key.id() + '/' + utilities.generateid_for_users(word)
                anagram_key = ndb.Key(MyList, anagram_id)
                my_list = anagram_key.get()

                if my_list:
                    utilities.addtoanagram(word, wordsinfo, anagram_key)
                else:
                    utilities.addanagram_new(my_user, word, wordsinfo, anagram_id, anagram_key)

                readLine = openFile.readline()

            openFile.close()
            self.redirect('/')

        if button == 'Search':
            search_result = self.search(input_text, my_user)
            renderer.render_search(self, input_text, search_result)
        elif button == 'Generate':
            words = self.generate(input_text, my_user)
            renderer.render_search(self, input_text, words)

    def search(self, text, my_user):
        anagram_id = my_user.key.id() + '/' + utilities.generateid_for_users(text)
        mylist = ndb.Key(MyList, anagram_id).get()

        if mylist:
            result = mylist.words
            result.remove(text)
            return result
        else:
            return None

    def generate(self, input_text, my_user):
        permutations = utilities.a_permutations(input_text)
        my_list = MyList.query().fetch()
        sorted_list= []
        result = []
        for i in range(len(my_list)):
            sorted_list.append(my_list[i].sorted_word)
        for i in permutations:
            for j in sorted_list:
                if i == j:
                    anagram_id = my_user.key.id() + '/' + j
                    mylist = ndb.Key(MyList, anagram_id).get()
                    for x in mylist.words:
                        result.append(str(x))
        if input_text in result:
            result.remove(input_text)
        return result

app = webapp2.WSGIApplication(
    [
        ('/', MainPage),
        ('/add', Add)
    ], debug=True)
