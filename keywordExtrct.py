#!/usr/bin/env python
# coding: utf-8

# In[3]:


import glob
import pandas as pd
import xml.etree.cElementTree as et
from xml.etree.cElementTree import iterparse
from time import process_time 
import os

# Start the stopwatch / counter  
t1_start = process_time() 

def getvalueofnode( node ):
    return node.text if node is not None else None

def getnumberofnode( node ):
    return int(node.text) if node is not None else 0

for filename in glob.glob(r'/home/PubMed/*.xml'):
    with open(filename, 'r', encoding="utf-8") as content:
        print(filename)
        parsedXML = et.parse(content)
        items = []
        
        '''
        PMID
        DateCompleted
        JournalPubDate
        JournalTitle
        ISOAbbreviation
        ArticleTitle
        Language
        JournalCountry
        ArticleID
        KeywordList
        '''
        
        for node in parsedXML.getroot():
            PMID = node.find('MedlineCitation/PMID')
            DateCompleted = node.find('MedlineCitation/DateCompleted/Year')


            JournalPubDate = node.find('MedlineCitation/Article/Journal/JournalIssue/PubDate/Year')
            JournalTitle = node.find('MedlineCitation/Article/Journal/Title')
            ISOAbbreviation = node.find('MedlineCitation/Article/Journal/ISOAbbreviation')
            ArticleTitle = node.find('MedlineCitation/Article/ArticleTitle')    
            
            Language = node.find('MedlineCitation/Article/Language')
            
            JournalCountry = node.find('MedlineCitation/MedlineJournalInfo/Country')
            
            # MeshHeadingList
            ArticleID = node.find('PubmedData/ArticleIdList/ArticleId')
            
            # KeywordList
            KeywordList = node.find('MedlineCitation/KeywordList')
            

            
            keywords = []
            if KeywordList is not None:
                for Keyword in KeywordList:
                    if Keyword is not None:
#                        keywords.append(Keyword.text)
                        print(Keyword.text)

       
                        item = [getvalueofnode(PMID), getvalueofnode(DateCompleted), 
                            getvalueofnode(JournalPubDate), getvalueofnode(JournalTitle), getvalueofnode(ISOAbbreviation), 
                            getvalueofnode(ArticleTitle), getvalueofnode(Language), 
                            getvalueofnode(JournalCountry), getvalueofnode(ArticleID), Keyword.text]
        
                        items.append(item)
            
            
#            print(filename)
            df = pd.DataFrame(items, columns = ['PMID', 'DateCompleted', 'JournalPubDate', 
                                                'JournalTitle', 'ISOAbbreviation', 'ArticleTitle', 'Language', 
                                                'JournalCountry', 'ArticleID', 
                                                'KeywordList'])
            
        

        df.to_csv(r'/home/PubMed/keyword.csv', mode = 'a', header = True)



# Stop the stopwatch / counter 
t1_stop = process_time() 
   
print("Elapsed time:", t1_stop, t1_start)  
print("Elapsed time during the whole program in seconds:", t1_stop-t1_start) 







