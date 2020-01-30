#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nltk
#from nltk.corpus import stopwords
import re
import matplotlib
from nltk.collocations import *
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
import math


italianStopwords=['ad',
 'al',
 'allo',
 'ai',
 'agli',
 'all',
 'agl',
 'alla',
 'alle',
 'con',
 'col',
 'coi',
 'da',
 'dal',
 'dallo',
 'dai',
 'dagli',
 'dall',
 'dagl',
 'dalla',
 'dalle',
 'di',
 'del',
 'dello',
 'dei',
 'degli',
 'dell',
 'degl',
 'della',
 'delle',
 'in',
 'nel',
 'nello',
 'nei',
 'negli',
 'nell',
 'negl',
 'nella',
 'nelle',
 'su',
 'sul',
 'sullo',
 'sui',
 'sugli',
 'sull',
 'sugl',
 'sulla',
 'sulle',
 'per',
 'tra',
 'contro',
 'io',
 'tu',
 'lui',
 'lei',
 'noi',
 'voi',
 'loro',
 'mio',
 'mia',
 'miei',
 'mie',
 'tuo',
 'tua',
 'tuoi',
 'tue',
 'suo',
 'sua',
 'suoi',
 'sue',
 'nostro',
 'nostra',
 'nostri',
 'nostre',
 'vostro',
 'vostra',
 'vostri',
 'vostre',
 'mi',
 'ti',
 'ci',
 'vi',
 'lo',
 'la',
 'li',
 'le',
 'gli',
 'ne',
 'il',
 'un',
 'uno',
 'una',
 'ma',
 'ed',
 'se',
 'perché',
 'anche',
 'come',
 'dov',
 'dove',
 'che',
 'chi',
 'cui',
 'non',
 'più',
 'quale',
 'quanto',
 'quanti',
 'quanta',
 'quante',
 'quello',
 'quelli',
 'quella',
 'quelle',
 'questo',
 'questi',
 'questa',
 'queste',
 'si',
 'tutto',
 'tutti',
 'a',
 'c',
 'e',
 'i',
 'l',
 'o',
 'ho',
 'hai',
 'ha',
 'abbiamo',
 'avete',
 'hanno',
 'abbia',
 'abbiate',
 'abbiano',
 'avrò',
 'avrai',
 'avrà',
 'avremo',
 'avrete',
 'avranno',
 'avrei',
 'avresti',
 'avrebbe',
 'avremmo',
 'avreste',
 'avrebbero',
 'avevo',
 'avevi',
 'aveva',
 'avevamo',
 'avevate',
 'avevano',
 'ebbi',
 'avesti',
 'ebbe',
 'avemmo',
 'aveste',
 'ebbero',
 'avessi',
 'avesse',
 'avessimo',
 'avessero',
 'avendo',
 'avuto',
 'avuta',
 'avuti',
 'avute',
 'sono',
 'sei',
 'è',
 'siamo',
 'siete',
 'sia',
 'siate',
 'siano',
 'sarò',
 'sarai',
 'sarà',
 'saremo',
 'sarete',
 'saranno',
 'sarei',
 'saresti',
 'sarebbe',
 'saremmo',
 'sareste',
 'sarebbero',
 'ero',
 'eri',
 'era',
 'eravamo',
 'eravate',
 'erano',
 'fui',
 'fosti',
 'fu',
 'fummo',
 'foste',
 'furono',
 'fossi',
 'fosse',
 'fossimo',
 'fossero',
 'essendo',
 'faccio',
 'fai',
 'facciamo',
 'fanno',
 'faccia',
 'facciate',
 'facciano',
 'farò',
 'farai',
 'farà',
 'faremo',
 'farete',
 'faranno',
 'farei',
 'faresti',
 'farebbe',
 'faremmo',
 'fareste',
 'farebbero',
 'facevo',
 'facevi',
 'faceva',
 'facevamo',
 'facevate',
 'facevano',
 'feci',
 'facesti',
 'fece',
 'facemmo',
 'faceste',
 'fecero',
 'facessi',
 'facesse',
 'facessimo',
 'facessero',
 'facendo',
 'sto',
 'stai',
 'sta',
 'stiamo',
 'stanno',
 'stia',
 'stiate',
 'stiano',
 'starò',
 'starai',
 'starà',
 'staremo',
 'starete',
 'staranno',
 'starei',
 'staresti',
 'starebbe',
 'staremmo',
 'stareste',
 'starebbero',
 'stavo',
 'stavi',
 'stava',
 'stavamo',
 'stavate',
 'stavano',
 'stetti',
 'stesti',
 'stette',
 'stemmo',
 'steste',
 'stettero',
 'stessi',
 'stesse',
 'stessimo',
 'stessero',
 'stando']
englishStopwords=['i',
 'me',
 'my',
 'myself',
 'we',
 'our',
 'ours',
 'ourselves',
 'you',
 "you're",
 "you've",
 "you'll",
 "you'd",
 'your',
 'yours',
 'yourself',
 'yourselves',
 'he',
 'him',
 'his',
 'himself',
 'she',
 "she's",
 'her',
 'hers',
 'herself',
 'it',
 "it's",
 'its',
 'itself',
 'they',
 'them',
 'their',
 'theirs',
 'themselves',
 'what',
 'which',
 'who',
 'whom',
 'this',
 'that',
 "that'll",
 'these',
 'those',
 'am',
 'is',
 'are',
 'was',
 'were',
 'be',
 'been',
 'being',
 'have',
 'has',
 'had',
 'having',
 'do',
 'does',
 'did',
 'doing',
 'a',
 'an',
 'the',
 'and',
 'but',
 'if',
 'or',
 'because',
 'as',
 'until',
 'while',
 'of',
 'at',
 'by',
 'for',
 'with',
 'about',
 'against',
 'between',
 'into',
 'through',
 'during',
 'before',
 'after',
 'above',
 'below',
 'to',
 'from',
 'up',
 'down',
 'in',
 'out',
 'on',
 'off',
 'over',
 'under',
 'again',
 'further',
 'then',
 'once',
 'here',
 'there',
 'when',
 'where',
 'why',
 'how',
 'all',
 'any',
 'both',
 'each',
 'few',
 'more',
 'most',
 'other',
 'some',
 'such',
 'no',
 'nor',
 'not',
 'only',
 'own',
 'same',
 'so',
 'than',
 'too',
 'very',
 's',
 't',
 'can',
 'will',
 'just',
 'don',
 "don't",
 'should',
 "should've",
 'now',
 'd',
 'll',
 'm',
 'o',
 're',
 've',
 'y',
 'ain',
 'aren',
 "aren't",
 'couldn',
 "couldn't",
 'didn',
 "didn't",
 'doesn',
 "doesn't",
 'hadn',
 "hadn't",
 'hasn',
 "hasn't",
 'haven',
 "haven't",
 'isn',
 "isn't",
 'ma',
 'mightn',
 "mightn't",
 'mustn',
 "mustn't",
 'needn',
 "needn't",
 'shan',
 "shan't",
 'shouldn',
 "shouldn't",
 'wasn',
 "wasn't",
 'weren',
 "weren't",
 'won',
 "won't",
 'wouldn',
 "wouldn't"]
#global clearedText
#clearedText=''


#TOKENIZEDTEXT take a text and return a list of token such as ['name','todd','engineer','worked'], clearing the text
  #input: text
  #output: list of  tokens
def tokenizedText(text):   
    
    
    clearedText=''
    text=nltk.wordpunct_tokenize(text)
    punctToClear=['•','http','|','.',',','-','_','','?','!','"','–',':',';',
                  'da-a','(',')','(da-a)',"'",'/','’',"),","”",
                  "date","nome","principali",'indirizzo','lavoro','azienda','tipo',
                  '“',"presso","svolto",').','&','settore','corso','personali','attività',
                  'impiego','responsabilità','datore','mansioni','studi','istruzione','svolto',
                  "svolte","curriculum","vitae",'%','➢','durante','▪',"gennaio","febbraio",
                  "marzo","aprile","maggio","giugno","luglio","agosto","settembre","ottobre",
                  "novembre","dicembre",'@','$'
                  ]
    text=[i for i in text if i not in punctToClear]
    r = re.compile(r'\D') #filter numbers
    text=list(filter(r.match,text))
    countEnglish=0
    countItalian=0
    for i in text:
        if i in italianStopwords:
            countItalian+=1
        if i in englishStopwords:
            countEnglish+=1
    print('ita'+str(countItalian))
    print('eng'+str(countEnglish))
    if countEnglish>countItalian:
        text=[i for i in text if i not in englishStopwords]
        print('Language is: English')
        clearedText=text
    if countEnglish<countItalian:
        text=[i for i in text if i not in italianStopwords]
        print('Language is: Italian')
        clearedText=text
    if countEnglish==countItalian:
        print("Can't detect language")
        clearedText=text
    if countEnglish==0 and countItalian==0:
        clearedText=text
    
    return clearedText
    
        

#MOSTRCOMMON take a tokenizedText and return a list of tuple with (TERM,ABSOLUTE FREQ) 
    #input: list of token
    #output: list  of tuple
    
def mostCommon(text='',n=10):
    fdist1=nltk.FreqDist(text)
    return fdist1.most_common(n)


def plotMostCommon(text='',n=10,cumulative=False):
    fdist1=nltk.FreqDist(text)
    plot=fdist1.plot(n,cumulative=cumulative)
    return plot


def collocationBigram(text='',n=4):
    
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(text)
    scored = finder.score_ngrams(bigram_measures.raw_freq)
    return sorted(finder.nbest(bigram_measures.raw_freq, n))

def collocationTrigram(text='',n=4):
    
    trigram_measures = nltk.collocations.TrigramAssocMeasures()
    finder = TrigramCollocationFinder.from_words(text)
    scored = finder.score_ngrams(trigram_measures.raw_freq)
    return sorted(finder.nbest(trigram_measures.raw_freq, n))



def plotCollScoreBigram(text='',n=4):
    
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(text)
    scored = finder.score_ngrams(bigram_measures.raw_freq)
    bigram=[]
    ranking=[]
    for i in scored:
        bigram.append(str(i[0]))
        ranking.append(i[1])
    plt.plot(bigram[:n],ranking[:n])
    

def plotCollScoreTrigram(text='',n=4):
    
    trigram_measures = nltk.collocations.TrigramAssocMeasures()
    finder = TrigramCollocationFinder.from_words(text)
    scored = finder.score_ngrams(trigram_measures.raw_freq)
    trigram=[]
    ranking=[]
    for i in scored:
        trigram.append(str(i[0]))
        ranking.append(i[1])
    plt.plot(trigram[:n],ranking[:n])
    



def tag(text):
    
    text=nltk.word_tokenize(text)
    tagged=nltk.pos_tag(text)
    return tagged
    #CC=conjuntion (and, but, or)
    #RB=adverbs
    #IN=preposition
    #NN=noun
    #JJ=adjective
    #for documentation, for example, nltk.help.upenn_tagset('RB')
    #NB: it works in English only 
    


def tf(text):
    
    #TF takes a list of tokens and return a dictionary with {word:relative frequency}
    #TF is the time of occurency of a term in a document compared to total number of terms in that document. tf=t_i/t_tot
    #usage: tf.get('word') to know how frequent is the word across a specific document (text)
       #input:list of tokens
       #output: dictionary
    tf={}
    for i in text:
        tf[i]=text.count(i)/len(text)
        
    sortedList=sorted(tf.items(),key=lambda x:x[1],reverse=True)
    tf={}
    for i in sortedList:
        
        tf[i[0]]=i[1]
        
    return tf



def idf(corpus,words):
    
    
    
    #IDF takes a corpus (list of tokenized lists) as input and return a dict with {word:score} for
    #every word in a document. Note that len(idf)==len(tf) and this is useful in order to
    #calculate the tf-idf. 
    #IDF tells us how rare is a word across the entire corpus. Inverse data frequency
    #it is the total number of document in relationship with the number of document
    #containing the term. Every word of the  document are take into consideration and
    #the function check if every word is contained in the corpus
      #input list of lists of tokens for corpus 
      #input list of tokens for words > this take a tokenizedText of a single Document
      #output dictionary
    
    words=list(dict.fromkeys(words)) #remove duplicates from list
    N=len(corpus) #N=total number of  document
    d_w={}#d_w=number of document containing the word of which we want to calculate idf   
    
    for document in corpus:
        for word_to_search in words:
            if word_to_search  in document:
                if word_to_search in d_w.keys():
                    d_w[word_to_search]+=1
                else:
                    d_w[word_to_search]=1
    for i in words:
        if i not in d_w.keys():
            d_w[i]=0
    
    for i in d_w.keys():
        if d_w.get(i)!=0:
            d_w[i]=math.log10(N/float(d_w.get(i)))
    
    idf={}
    sortedList=sorted(d_w.items(),key=lambda x:x[1],reverse=True)
    for i in sortedList:
        idf[i[0]]=i[1]
    return idf


# TF_IDF takes a corpus (list of tokenized lists) as input and return a dict with {word:score} for
#every word in a document.
#It "weights" term frequency whit inverse document frequency and can be used to get roughly tags. 
#Every word of the  document are taked into consideration and
#the function check if every word is contained in the corpus. 
    #input list of lists of tokens for corpus 
    #input list of tokens for words > this take a tokenizedText of a single Document
    #output dictionary
    
                    
def tf_idf(corpus,document):
    
    termFreq=tf(document)    
    inverseDocFreq=idf(corpus,document)
    tf_idf={}
    for i in termFreq.keys():
        tf_idf[i]=termFreq.get(i)*inverseDocFreq.get(i)
    
    scored_value={}
    sortedList=sorted(tf_idf.items(),key=lambda x:x[1],reverse=True)
    for i in sortedList:
        scored_value[i[0]]=i[1]
    return scored_value


# GETTAG simply returns the first 5 scored value of tf_idf for a certain document

def getTag(corpus,document):
    
    tf_idf_dict=tf_idf(corpus,document)
    return list(tf_idf_dict)[0:5]
    
























    
        
       
