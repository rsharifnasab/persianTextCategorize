import os
import bs4
def get_file_list():
    input_files = os.listdir("./corpus") #main files
    input_files = os.listdir("./tmp") # just temp files
    xml_files = []
    for f in input_files :
        if ".xml" in f: xml_files.append(f)


file_list = get_file_list()
