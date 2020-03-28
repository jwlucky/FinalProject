#!/usr/bin/env python
# coding: utf-8

# In[2]:


import glob
import pandas as pd
import xml.etree.cElementTree as et
from xml.etree.cElementTree import iterparse
from time import process_time
import os
import datetime
import dateutil.parser
from dateutil.parser import parse

# Start the stopwatch / counter
t1_start = process_time()

def getvalueofnode( node ):
    return node.text if node is not None else None

def getyearofnode( node ):
    return node.text if node is not None else None


def getnumberofnode( node ):
    return int(node.text) if node is not None else 0

for filename in glob.glob(r'E:\winter 2020\step 12\pubmedsample.xml'):
    with open(filename, 'r', encoding="utf-8") as content:
        # output processing logs
        print(filename)
        parsedXML = et.parse(content)
        items = []

        '''
        PMID
        JournalPubDate
        JournalTitle
        ArticleTitle
        Language
        JournalCountry
        ReferenceList
        '''
        for node in parsedXML.getroot():
            PMID = node.find('MedlineCitation/PMID')
            JournalPubDate = node.find('MedlineCitation/Article/Journal/JournalIssue/PubDate')
            Year = node.find('MedlineCitation/Article/Journal/JournalIssue/PubDate/Year')
            MedlineDate = node.find('MedlineCitation/Article/Journal/JournalIssue/PubDate/MedlineDate')

            if JournalPubDate is not None:
                if Year is not None:
                    JournalPubDate = Year.text
                elif MedlineDate is not None:
                    JournalPubDate = MedlineDate.text[0:4];
                    print(MedlineDate.text)

            JournalTitle = node.find('MedlineCitation/Article/Journal/Title')
            ArticleTitle = node.find('MedlineCitation/Article/ArticleTitle')
            Language = node.find('MedlineCitation/Article/Language')
            JournalCountry = node.find('MedlineCitation/MedlineJournalInfo/Country')

            ReferenceList = node.find('PubmedData/ReferenceList')
            references = []
            if ReferenceList is not None:
                for reference in ReferenceList:
                    if reference is not None:
                       referenceID = reference.find('ArticleIdList/ArticleId');
                    references.append(getvalueofnode(referenceID));
            # count how many references in ReferenceList row
            countReferences = len(references)
            item = [getvalueofnode(PMID),
                    JournalPubDate, getvalueofnode(JournalTitle),
                    getvalueofnode(ArticleTitle), getvalueofnode(Language),
                    getvalueofnode(JournalCountry), references,
                    countReferences]
            items.append(item)

            df = pd.DataFrame(items, columns = ['PMID', 'JournalPubDate',
                                                'JournalTitle', 'ArticleTitle', 'Language',
                                                'JournalCountry',
                                                'ReferenceList', 'countReferences'])

        print(df)

        df.to_csv(r'E:\winter 2020\step 12\test output\testSample19.csv', index=False, mode = 'a', header = True)

# Stop the stopwatch / counter
t1_stop = process_time()
print("Elapsed time:", t1_stop, t1_start)
print("Elapsed time during the whole program in seconds:", t1_stop-t1_start)

