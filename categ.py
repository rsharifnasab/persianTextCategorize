import os
from bs4 import BeautifulSoup
from collections import defaultdict

pre_add = "./tmp"

class Word():
    """docstring for Word."""

    word = ""
    #keys =

    def __init__(self, word):
        self.word = word

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

    def __clear_key__(self):
        try:
            dot_index = self.key.index(".")
            self.key = self.key[:dot_index]
        except:
            pass

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


file_list = get_file_list()
all_corpus = []
for xml_file in file_list:
    all_corpus += parse(xml_file)

db = defaultdict(lambda: [])
for i in all_corpus:
    db[i.key] = i
for key in db.keys():
    print(key)
