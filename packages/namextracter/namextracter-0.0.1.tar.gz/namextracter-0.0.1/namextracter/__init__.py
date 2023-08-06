from nltk.corpus import wordnet
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import re
from nltk.tag import pos_tag
class namextract:
    cnames = []
    replacingwords = ['.', '-']
    Punclist = ['’','“','”','would','could','since']
    stop_words = stopwords.words('english') +  list(string.punctuation) + Punclist
        
        
    def names(self,text):
        compiles = re.compile('|'.join(map(re.escape, self.replacingwords)))
        uptex = compiles.sub(" ", text)
        twords = word_tokenize(uptex)
        
        names = {}
        nums = {}
        for n,word in enumerate(twords):
            if word.lower() not in self.stop_words:
                if word.isnumeric():
                    nums[n] = word
                if (len(wn.synsets(word)) == 0 and not word.isnumeric()) or word in self.cnames: #or check if name in common list of words
                    names[n]=word
        return names
    
    def pos_tag_names(self,text): 
        na ={}
        tags = pos_tag(text.split())
        for n,word in enumerate(tags):
            if tags[n][1] == 'NNP':
                if word[0].lower() not in self.stop_words:
                    na[n] = word[0]
        return na
    
    
    #this fuction takes the names dictionary from names fuction and joins these
    #names based on the position of then in text
    
    #this fuction returns a set of all joined names
    
    
    def fullnames(self,na):
        lis = list(na.keys())
    
        fullnames = {}
        for k in lis:
            fullnames[k] = na[k]
            if k+1 in lis:
                fullnames[k] = fullnames[k] + " " + na[k+1]
                lis.remove(k+1)
            if k+2 in lis:
                fullnames[k] = fullnames[k] + " " + na[k+2]
                lis.remove(k+2)
                
        #uncomment below code if names have more than 3 words
        #     if k+3 in lis:
        #         fullnames[k] = fullnames[k] + na[k+3]
        #         lis.remove(k+3)
        
        return set(fullnames.values())    
    def __init__(self,namelist=[]):
        self.cnames = namelist
        return
 