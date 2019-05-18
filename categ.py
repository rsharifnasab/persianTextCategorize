import os
from bs4 import BeautifulSoup
from collections import defaultdict
import pickle
pre_add = "./tmp"
pre_add = "./corpus"
junk_words = [" ","ز","بود","که","و","هاي","ها","مثل","شود","این","آن","ان","همین","بود","نیست","شد","کرد"]
junk_chars = ["(",")","1","2","3","4","5","6","7","8","9","0"]
def is_not_valid_word(word):
    if word in junk_words: return True
    if len(word) < 4: return  True
    for junk_char in junk_chars:
        if junk_char in word: return True

    return False

def save_obj(obj, name):
    with open('obj/'+ name + '.db', 'wb') as f:
        pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('obj/' + name + '.db', 'rb') as f:
        return pickle.load(f)


def save_word_list(obj):
    save_obj(obj,"words")

def load_word_list():
    return load_obj("words")


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


def get_file_list():
    input_files = os.listdir(pre_add)
    xml_files = []
    for f in input_files :
        if ".xml" in f: xml_files.append(f)
    print(" count if files:" ,len(xml_files))
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

def make_word_list(all_corpus):
    word_list = {}
    for corpus in all_corpus:
        for word in corpus.text.split(" "):
            if is_not_valid_word(word): continue
            if word not in word_list.keys(): # make new Word and add it to word_list
                new_word = Word(word)
                word_list[word] = new_word
        #print("word:"+word + " key is: " , corpus.key)
            if corpus.key not in word_list[word].tekrar.keys():
                    word_list[word].tekrar[corpus.key] = 0
            word_list[word].tekrar[corpus.key]+=1
    return word_list

def is_word_frequent(word):
    return True # TODO
    if sum(word.tekrar.values()) < 3: return False
    return True
def clean_word_list(word_list):
    word_list = {key: value for key, value in word_list.items() if is_word_frequent(value)}
    return word_list

#main program
all_corpus = get_all_corpus()
db = get_text_by_key(all_corpus)
word_list = make_word_list(all_corpus)
word_list = clean_word_list(word_list)
for word in word_list.values():
    print("لغت: ",word.word)
    for key in word.tekrar.keys():
        print(key+":",word.tekrar[key]);
    print("----\n")
print("len = ",len(word_list.values()))


save_word_list(word_list)
#wl2 = load_word_list()
