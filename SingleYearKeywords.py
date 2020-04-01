import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline
import re
from glob import glob
import os

filenames = [r'testSample2.csv',
             r'testSample3.csv']

data = []
for filename in filenames:
    print(filename)
    df = pd.read_csv(filename, index_col=None, header=0)
    data.append(df)
df = pd.concat(data, axis=0, ignore_index=True)
df['MeshHeadingList'] = df.MeshHeadingList.str.lower()
df['JournalPubDate'] = df.JournalPubDate.astype(str)

filtered = df[df['JournalPubDate']== '2000']
print(filtered)

groupedKeywords = filtered.groupby('MeshHeadingList')['JournalCountry'].count().sort_values(ascending=False).index[:10]
print(groupedKeywords)
filtered = filtered.loc[filtered['MeshHeadingList'].isin(groupedKeywords)]
filtered['num']=1
print(filtered)

keywordChanges = filtered.pivot_table('num', index='JournalPubDate',
                                columns='MeshHeadingList',aggfunc=sum).fillna(0)
print(keywordChanges)

