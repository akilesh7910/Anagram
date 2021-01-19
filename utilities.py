from google.appengine.ext import ndb
from google.appengine.api import users
from myuser import MyUser
from mylist import MyList
import re
from itertools import permutations

with open("wordsEn.txt") as word_file:
    english_words = set(word.strip().lower() for word in word_file)

def getloginurl(main_page):
    return users.create_login_url(main_page.request.url)

def getlogouturl(main_page):
    return users.create_logout_url(main_page.request.url)

def get_user():
    return users.get_current_user()

def getuser():
    user = get_user()
    if user:
        my_user_key = ndb.Key(MyUser, user.user_id())
        return my_user_key.get()

def user_loggedin():
    return True if get_user() else False

def existing_user():
    return True if getuser() else False

def add_new_user(user):
    MyUser(id=user.user_id()).put()

def preparetextinput(input_text):
    result = input_text.lower()
    result = re.sub('[^a-z]+', '', result)
    return result

def getanagrams_from_user(my_user):
    if my_user:
        result = []
        word_Count, total_Count = 0, 0
        for mylist in my_user.my_list:
            my_list = mylist.get()
            word_Count += 1
            total_Count += len(my_list.words)
            result.append(my_list)

        return result, word_Count, total_Count

def addanagram_new(my_user, text, words, anagram_id, anagram_key):
    if englishword(text):
        mylist = MyList(id=anagram_id)
        mylist.words.append(text)
        mylist.sorted_word = generateid_for_users(text)
        mylist.length = len(text)
        mylist.words_count = len(mylist.words)
        mylist.sub_words = words
        mylist.user_id = my_user.key.id()
        mylist.put()
        my_user.my_list.append(anagram_key)
        my_user.put()

def addtoanagram(text, words1, anagram_key):
    mylist = anagram_key.get()
    if text not in mylist.words:
        if englishword(text):
            mylist.words.append(text)
            mylist.words_count = len(mylist.words)
            for i in words1:
                mylist.sub_words.append(i)
            mylist.put()

def generateid_for_users(text):
    key = text.lower()
    return ''.join(sorted(key))

def a_permutations(input_string):
    result = [perm for length in range(1, len(input_string) + 1) for perm in permutations(input_string, length)]
    result = list(set(result))
    r = []
    for i in result:
        if len(i) >= 3:
            r.append(''.join(i))
    return r

def englishword(text):
    return True if text in english_words else False

def filterenglishwords(word_list):
    result = []
    for word in word_list:
        if word in english_words:
            if word not in result:
                result.append(word)

    return result
