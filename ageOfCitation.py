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

for filename in glob.glob(r'/*.xml'):
    with open(filename, 'r') as content:

        print(filename)
        parsedXML = et.parse(content)
        items = []

        '''
        PMID
        JournalPubDate
        CitationList
        CitationYear
        '''
        for node in parsedXML.getroot():
            PMID = node.find('MedlineCitation/PMID')
            JournalPubDate = node.find('MedlineCitation/Article/Journal/JournalIssue/PubDate')
            Year = node.find('MedlineCitation/Article/Journal/JournalIssue/PubDate/Year')
            MedlineDate = node.find('MedlineCitation/Article/Journal/JournalIssue/PubDate/MedlineDate')
            ReferenceList = node.find('PubmedData/ReferenceList')
#             Age = JournalPubDate - CitationYear

            if JournalPubDate is not None:
                if Year is not None:
                    JournalPubDate = Year.text
                elif MedlineDate is not None:
                    JournalPubDate = MedlineDate.text[0:4];
#                     print(MedlineDate.text)

            citationYear = 0
            if ReferenceList is not None:
                Citation = ReferenceList.findall('Reference/Citation')
                for c in Citation:
                    citationText = c.text
                    if citationText.find('.') > -1:
                        citationYear = citationText[citationText.find('.') + 1 : citationText.find('.') + 6]

                        item = [getvalueofnode(PMID), JournalPubDate, getvalueofnode(c), citationYear, int(JournalPubDate) - int(citationYear)]
                        items.append(item)

        df = pd.DataFrame(items, columns = ['PMID', 'JournalPubDate', 'CitationList', 'CitationYear','CitationAge'])
#        print(df)

    df.to_csv(r'/home/tian/PubMed/Step14/ageCi/AgeofCited25.csv', index=False, mode = 'a', header = False)

# Stop the stopwatch / counter


t1_stop = process_time()
print("Elapsed time:", t1_stop, t1_start)
print("Elapsed time during the whole program in seconds:", t1_stop-t1_start)
