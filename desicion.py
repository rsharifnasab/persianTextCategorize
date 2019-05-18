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
    address = input("please enter path of your file : ")
    text = open(address,"r")
    text = text.read()
    return text

#main program
word_list = load_word_list()
new_text = get_new_text_from_user()

for value in word_list.values():
    print(value,value.tekrar)
print("\n\n\nyour test was:\n",new_text)
