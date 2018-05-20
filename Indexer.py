from bs4 import BeautifulSoup
import string
import glob
import os
import csv
import nltk.data
from nltk.corpus import stopwords
nltk.download('stopwords')

def freqBasedIndex():
    docList = []
    docData = {}
    relWords = {'apple':[], 'steve_jobs':[], 'ipod':[], 'ipad':[], 'iphone':[], 'steve_wozniak':[], 'pixar':[], 'mac':[], 'macbook':[], 'siri':[]}
    #relWords.update( {'test':[]})
    print( relWords )
    n = 0
    path = 'C:/Users/Robert/Documents/School/Information Systems/IS392/project1/sites'
    for filename in glob.glob(os.path.join(path, '*.html')):
        n += 1
        docData = {'IndexNum': n, 'Name': filename }
        docList.append( docData )
    
    n = 0
    for docData in docList:
        n += 1
        #n=11
        #docData = docList[ 11 ]
        searchResults = {'apple':0, 'steve_jobs':0, 'ipod':0, 'ipad':0, 'iphone':0, 'steve_wozniak':0, 'pixar':0, 'mac':0, 'macbook':0, 'siri':0}

        fileName = docData['Name']
        print(str(n)+ " " + fileName )
        with open(fileName,'r') as file:
            htmlFile = file.read()

        soup = BeautifulSoup(htmlFile,"lxml")
        [s.extract() for s in soup('script')]
        text = soup.get_text()
        
        text = replacement(text)

        #Set StopWords (WIP)
        stops = set(stopwords.words('english'))

        tokens = [i for i in text.lower().split() if i not in stops]
        #tokens = text.lower().split()
        for t in tokens:
            if t.find("\\u") >= 0 or t.find('http') >=0 or t.find('#x') >=0:
                continue
            if t in searchResults:
                searchResults[t] += 1
            else:
                searchResults.update({t:1})
                #relWords.update( {t:[]})

        #print( searchResults )
        for i in searchResults:
            val = searchResults[i]
            if val > 0:
                if i in relWords:
                    #print(str(val) + " " + i)
                    rList = relWords[i]
                    rList.append( [ n, val])
                    relWords.update( {i:rList})
                else:
                    relWords.update({i:[[n, val]]})
                    
       
    with open('C:/Users/Robert/Documents/School/Information Systems/IS392/Indexer-RobertSlawinski/output.txt', 'w', encoding='utf8') as f:
        for key, value in relWords.items():
            f.write('%s:%s\n' % (key, value))
    
    wordList = []
    for key, value in relWords.items():  
        wordList.append( key )
            
    with open('C:/Users/Robert/Documents/School/Information Systems/IS392/Indexer-RobertSlawinski/wordlist.txt', 'w', encoding='utf8') as f:
        for x in sorted(wordList):
        #for key, value in relWords.items():
            f.write('%s\n' % (x))
    #print( relWords )
    print("Done!")
def replacement(text):
        text = text.replace('\\', ' ')
        text = text.replace('\\t', ' ')
        text = text.replace('\\n', '')
        text = text.replace('(', ' ')
        text = text.replace(')', ' ')
        text = text.replace(',', ' ')
        text = text.replace(';', ' ')
        text = text.replace('\"', ' ')
        text = text.replace('/', ' ')
        text = text.replace('\'', ' ')
        text = text.replace('.',' ')  
        text = text.replace('?', ' ')
        text = text.replace('!', ' ')
        text = text.replace('[', ' ')
        text = text.replace(']', ' ')
        text = text.replace('-', ' ')
        text = text.replace('<', ' ')
        text = text.replace('>', ' ')
        text = text.replace('>', ' ')
        text = text.replace('#', ' ')
        text = text.replace('&', ' ')
        text = text.replace('%', ' ')
        text = text.replace('$', ' ')
        text = text.replace(':', ' ')
        text = text.replace('*', ' ')
        text = text.replace('+', ' ')
        text = text.replace('_', ' ')
        text = text.replace('=', ' ')
        text = text.replace('@', ' ')
        text = text.replace('`', ' ')
        text = text.replace('^', ' ')
        text = text.replace('~', ' ')
        text = text.replace('|', ' ')
        text = text.replace('{', ' ')
        text = text.replace('}', ' ')
        text = text.replace('steve jobs', 'steve_jobs')
        text = text.replace('steve wozniak', 'steve_wozniak')
        text = ' '.join(text.split())
        return text
def posBasedIndex():
    docList = []
    docData = {}
    relWords = {'apple':[], 'steve_jobs':[], 'ipod':[], 'ipad':[], 'iphone':[], 'steve_wozniak':[], 'pixar':[], 'mac':[], 'macbook':[], 'siri':[]}
    #relWords.update( {'test':[]})
    print( relWords )
    n = 0
    path = 'C:/Users/Robert/Documents/School/Information Systems/IS392/project1/sites2'
    for filename in glob.glob(os.path.join(path, '*.html')):
        n += 1
        docData = {'IndexNum': n, 'Name': filename }
        docList.append( docData )
        print(filename)
    n = 0
    for docData in docList:
        n += 1
        #n=11
        #docData = docList[ 11 ]
        searchResults = {'apple':0, 'steve_jobs':0, 'ipod':0, 'ipad':0, 'iphone':0, 'steve_wozniak':0, 'pixar':0, 'mac':0, 'macbook':0, 'siri':0}

        fileName = docData['Name']
        print(str(n)+ " " + fileName )
        with open(fileName,'r') as file:
            htmlFile = file.read()

        soup = BeautifulSoup(htmlFile,"lxml")
        [s.extract() for s in soup('script')]
        text = soup.get_text()
        
        text = replacement(text)

        #Set StopWords (WIP)
        stops = set(stopwords.words('english'))

        tokens = [i for i in text.lower().split() if i not in stops]
        #tokens = text.lower().split()
        for t in tokens:
            if t.find("\\u") >= 0 or t.find('http') >=0 or t.find('#x') >=0:
                continue
            if t in searchResults:
                searchResults[t] += 1
            else:
                searchResults.update({t:1})
                #relWords.update( {t:[]})

        #print( searchResults )
        for i in searchResults.keys():
            val = i
            #add document number and position
            
        
            position = htmlFile.find(val)
            while position != -1:
                
                if i in relWords:
                    #print(str(val) + " " + i)
                    rList = relWords[i]
                    rList.append( [ n, position])
                    relWords.update( {i:rList})
                else:
                    relWords.update({i:[[n, position]]}) 
                position = htmlFile.find(val, position+1)

       
    with open('C:/Users/Robert/Documents/School/Information Systems/IS392/Indexer-RobertSlawinski/positionOutput.txt', 'w', encoding='utf8') as f:
        for key, value in relWords.items():
            f.write('%s:%s\n' % (key, value))
    
    wordList = []
    for key, value in relWords.items():  
        wordList.append( key )
    #print( relWords )
    print("Done!")

posBasedIndex()
      
freqBasedIndex()