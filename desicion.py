import os,sys
import pickle

def load_obj(name):
    with open('obj/' + name + '.db', 'rb') as f:
        return pickle.load(f)

def load_word_list():
    print("loading database file from ./obj/words.db")
    try:
        return load_obj("words")
    except:
        print("could not load file, exitting")
        exit()

class Word():
    """docstring for Word."""

    word = ""
    tekrar = None
    def __init__(self, word):
        self.word = word
        self.tekrar = {} #defaultdict(lambda: 0)
    def __str__(self):
        return self.word;

class Corpus():
    """docstring for corpus."""
    key = ""
    title = ""
    text = ""

    def __init__(self,key,title,text):
        self.key = key.replace('\n','');
        self.title = title.replace('\n','');
        self.text = text.replace('\n','');
        self.__clear_key__()
        self.__clear_text__()


    def __clear_key__(self):
        try:
            dot_index = self.key.index(".")
            self.key = self.key[:dot_index]
        except:
            pass

    def __clear_text__(self):
        bad_chars = ["،",".",";",":",'"',"'"]
        for char in bad_chars:
            self.text = self.text.replace(char,'')


    def __str__(self):
        ans = "\nkey = " + self.key + ",\n title = " + self.title + ",\n text = " + self.text[:100]
        return ans;

def get_new_text_from_user():
    address = input("please enter path of your file : \n")
    text = open(address,"r")
    text = text.read()
    return text

def clear_word(text):
    bad_chars = ["،",".",";",":",'"',"'"]
    for char in bad_chars:
        text = text.replace(char,'')
    return text

def make_guess(new_text,word_list):
    guess = {}
    for word in new_text.split(" "):
        if word not in word_list: continue
        for key in word_list[word].tekrar.keys():
            if key not in guess.keys(): guess[key] = 0
            guess[key] += word_list[word].tekrar[key]
    return guess

def count_all(word_list):
    db = {}
    for word in word_list.keys(): #every word
        for key in word_list[word].tekrar.keys(): #every topic
            if key not in db.keys(): db[key] = 0
            db[key]+=1
    return db

#main program
word_list = load_word_list()
new_text = get_new_text_from_user()
new_text = clear_word(new_text)
all = count_all(word_list)
guess = make_guess(new_text,word_list)

normalized = {}
for key in guess.keys():
    normalized[key] = guess[key]/all[key]*100
tedad_kol = sum(normalized.values())

ans = {}
for key in normalized.keys():
    ans[key] = normalized[key]/tedad_kol * 100
sorted_ans =  sorted(ans, key=ans.__getitem__)
print()
for key in sorted_ans[::-1]:
    print(key , " : " , ans[key] , "%")
