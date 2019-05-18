import os
from bs4 import BeautifulSoup
from collections import defaultdict
import pickle
pre_add = "./tmp"


def save_obj(obj, name):
    with open('obj/'+ name + '.db', 'wb') as f:
        pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('obj/' + name + '.db', 'rb') as f:
        return pickle.load(f)


def save_word_list(obj):
    save_obj(obj,"words.db")

def load_word_list():
    return load_obj("words.db")


class Word():
    """docstring for Word."""

    word = ""
    tekrar = defaultdict(lambda: 0)
    def __init__(self, word):
        self.word = word
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


def get_file_list():
    input_files = os.listdir(pre_add)
    xml_files = []
    for f in input_files :
        if ".xml" in f: xml_files.append(f)
    return xml_files

def parse(xml_file):
    all = []
    file = open(pre_add + "/" + xml_file,"r")
    bs = BeautifulSoup(file, features='xml') # or file.content
    for doc in bs.findAll('DOC'):
        category = doc.CAT.string
        title = doc.TITLE.string
        text = doc.TEXT.string
        if text == None:
            continue
            #TODO

        corp = Corpus(category,title,text) #make new instance of Corpus
        all.append(corp)

    return all

def get_text_by_key(corpus):
    db = defaultdict(lambda: []) # all texts defined by keys
    for text in all_corpus:
        db[text.key] += [text]

def get_all_corpus():
    file_list = get_file_list()
    all_corpus = []
    for xml_file in file_list:
        all_corpus += parse(xml_file)
        return all_corpus

all_corpus = get_all_corpus()
db = get_text_by_key(all_corpus)

word_list = {}
for corpus in all_corpus:
    for word in corpus.text.split(" "):
            if word == " ": continue
            if word not in word_list.keys(): # make new Word and add it to word_list
                new_word = Word(word)
                word_list[word] = new_word
            print("word:"+word + " key is: " , corpus.key)
            word_list[word].tekrar[corpus.key]+=1


for word in word_list.values():
    print("لغت: ",word.word)
    for key in word.tekrar.keys():
        print(key+":",word.tekrar[key]);
    print("-"*10 + "\n\n")

save_word_list(word_list)
wl2 = load_word_list()
print(wl2)
