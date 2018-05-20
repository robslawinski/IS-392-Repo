import glob
from bs4 import BeautifulSoup
import string
import os
import csv
import yaml
import ast
import json

#Variables
I = []
Index = 'C:/Users/Robert/Documents/School/Information Systems/IS392/Assignment 4/output.txt'
index = {}
totalDocs = 557
H = {}
relTerms = ['apple','steve_jobs', 'ipod', 'ipad','iphone','steve_wozniak','pixar','mac','macbook','siri',
           'first','awards','masterpiece','produced','early','directed','company','computer','american','foundation']
min_sup = 0.1
min_conf = 0.2

def needMerge(i1,i2):
    print("NeedMerge")
    print("ItemSet1: " + str(i1))
    print("ItemSet2: " + str(i2))
    for i in range(0,len(i1)-1):
        if i1[i] != i2[i]:
            return False
    #
    #Avoid if last two entries are identical
    #
    if len(i1) > 0 and len(i2) > 0:
        temp1 = i1.copy()
        temp2 = i2.copy()
        if temp1.pop() == temp2.pop():
            return False
    return True

def checkDuplicates(itemSetOne, freqItemSet):
    for i in range(0,len(itemSetOne)-1):
        item = itemSetOne[i]
        for j in range(0,len(itemSetOne)-1):
            if j != i:
                itemTwo = itemSetOne[j]
                if item == itemTwo:
                    return False
    
    for itemSet in freqItemSet:
        if itemSetOne == itemSet:
            return False
    return True

def merge(i1,i2):
    i3 = i1.copy()
    if len(i2) > 0:
        temp = i2.copy()
        i3.append(temp.pop())
    print("Merge: " + str(i3))
    
    return i3

def getSup(itemSet, ind, H):
    print("itemSet: " + str(itemSet))
    #print("H: " + str(H))

    if str(itemSet) in H:
        print("in H: " + str(H[str(itemSet)]))
        return H[str(itemSet)]
    inverted_lists = []
    intersectionList = []
    #print("get Sup: ")
    
    for item in itemSet:
        #print("item: " + item)
        for indexItem in ind:
            #print("indexItem: "+indexItem)
            if indexItem in item:
                inverted_lists.append(ind[item])
                # print("value: " + str(len(ind[item])))
    
    if len(inverted_lists) > 0:  
        intersectionList = set.intersection(*map(set,inverted_lists))
    else:
        return 0
    #print("Intersection List" + str(len(intersectionList)))
    #print( "Inverted Len: " + str(len(inverted_lists)))
    print("Get Support: " + str(itemSet) + " " + str((len((intersectionList))/totalDocs)))
    print("\n")
    sup = len((intersectionList))/totalDocs
    H[str(itemSet)] = sup
    return sup

def associationRuleMining(Index, T):
    index = transform(Index, T)
    #print("index: " + str(index))
    tokenCount = len(T)
    freqItemSet = [[] for i in range(1,tokenCount)]
    print("frequent Item Set 0: " + str(freqItemSet))
    #create initial frequent itemset of one item in each set.
    for term in T:
        #print("Term: " + term)
        I = [term]
        support = getSup(I, index,H)
        #print( str(I) + "support : " + str(support))
        if support > min_sup:
            freqItemSet[1].append(I)    
    print("frequent Item Set 1: " + str(freqItemSet))
    
    for itemSetNum in range(2, tokenCount):
    #for itemSetNum in range(2, 5):
        prevItemSets = freqItemSet[itemSetNum-1].copy()
        #print("prevItemSets: " + str(prevItemSets))
        n = len(prevItemSets)
        for i in range(1, n-1):  #was n-2
            for j in range(i+1, n): #was n-1
                itemSetOne = prevItemSets[i]
                itemSetTwo = prevItemSets[j]
                if needMerge(itemSetOne, itemSetTwo):
                    itemSetThree = merge(itemSetOne, itemSetTwo)
                    #if checkDuplicates(itemSetThree, freqItemSet[itemSetNum]):
                    support = getSup(itemSetThree, index,H) 
                    if support > min_sup:
                        freqItemSet[itemSetNum].append(itemSetThree)

            if len(freqItemSet[itemSetNum]) == 0:
                print("No New Itemsets")
                break
    with open('C:/Users/Robert/Documents/School/Information Systems/IS392/Assignment 4/support_file.txt', 'w', encoding='utf8') as d:
        for value in freqItemSet:
            d.write('%s\n' % (value))
    
    print(str(itemSetNum) + " freqItemSet: " + str(freqItemSet))
    
    rules = []
    for itemSetNum in range (2, tokenCount):
    #for itemSetNum in range (2, 5):
        if len(freqItemSet[itemSetNum]) == 0:
            break
        for itemSetOne in freqItemSet[itemSetNum]:
            for i in range(0,itemSetNum):
                itemSetTwo = itemSetOne.copy()
                itemSetTwo.remove(itemSetOne[i])
                supportDen = getSup(itemSetTwo, index,H)
                supportNum = getSup(itemSetOne, index,H)
                conf = supportNum/supportDen
                if conf > min_conf:
                    rule = []
                    rule.append(itemSetTwo)
                    rule.append(itemSetOne[i])
                    rule.append(supportDen)
                    rule.append(conf)
                    rules.append(rule)
                print("rules: "+ str(rules))
    with open('C:/Users/Robert/Documents/School/Information Systems/IS392/Assignment 4/output_file.txt', 'w', encoding='utf8') as f:
        for value in rules:
            f.write('%s\n' % (value))




associationRuleMining(Index, relTerms)

def transform(Index, T):
    tempIndex = {}
    with open(Index, 'r', encoding='utf8') as f:
        i = 0
        for line in f:
            #print(line)
            j = line.find(':')
            if j != -1:
                key = line[:j]
                if key in T:
                    array = line[j+1:]
                    ar = eval(array)
                    
                    #print(key)
                    #print(array)
                    #print(ar)
                    #print(len(ar))
                    newArray = []
                    for a in ar:
                        #print("a"+str(a))
                        newArray.append(a[0])
                    i+=1
                    tempIndex.update({key:newArray})
                    
            if i >= 20:
                break
    return tempIndex