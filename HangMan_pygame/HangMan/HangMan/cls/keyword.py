import random
import re
import string
import urllib.request
from bs4 import BeautifulSoup


class Keyword():

    keywords_list = None
    
    def __init__(self):
        self.keyword = ""
        self.hidden = ""
        self.space_indexes = []
    
    
    @classmethod
    def initialize_list(cls, keywords_list = None):
        if keywords_list is None:
            with urllib.request.urlopen("https://globalnews.ca/world/") as url:
                html = url.read()

            soup = BeautifulSoup(html, "lxml")

            h3 = soup.find_all("h3")
            keywords = []

            # remove spaces in the beginning of headlines and special characters not available in Alphabet()
            for i in range(11, 31):
                for c in h3[i].text:
                    if c.upper() in string.ascii_uppercase:
                        index = h3[i].text.find(c)
                        element = h3[i].text[index:].replace("\t", "").replace("\n", "")
                        
                        for c in element:
                            if c.upper() not in (string.ascii_uppercase + " "):
                                element.replace(c, "")
                        keywords.append(element)

                        break

            ## kill all script and style elements
            #for script in soup(["script", "style"]):
            #    script.extract()    # rip it out
            #
            ## get text
            #text = soup.get_text()
            #
            ## break into lines and remove leading and trailing space on each
            #lines = (line.strip() for line in text.splitlines())
            #
            ## break multi-headlines into a line each
            #chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            ## drop blank lines
            #text = '\n'.join(chunk for chunk in chunks if chunk)

            #keywords = text[692:2500].split("World\n")
            #
            #for k in keywords:
            #    for c in k:
            #        if c.upper() not in (string.ascii_uppercase+" "):
            #            k = k.replace(c, "")
            #
            
            cls.keywords_list = keywords

        else: cls.keywords_list = keywords_list


    def assign_new(self, keywords):

        self.keyword = keywords[random.randint(0, len(keywords)-1)].upper()
        self.hidden = self.keyword
        self.space_indexes = [m.start() for m in re.finditer(" ", self.keyword)]
        #while ''.join(set(keyword)).replace(" ", "") != ".":
        for c in self.hidden:
            if c in string.ascii_uppercase: self.hidden = self.hidden.replace(c, '_')


    def update(self, c):
        indexes = [m.start() for m in re.finditer(c.upper(), self.keyword)]

        for i in range(len(indexes)): 
            self.hidden = self.hidden[:indexes[i]] + c.upper() + self.hidden[indexes[i]+1:]
