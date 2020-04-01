import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline
import re
from glob import glob
import os


filenames = [r'testSample2.csv',
             r'testSample3.csv']

# Solution2 - read multiple csv
# Create the list for the three DataFrames you want to create:
data = []
for filename in filenames:
    print(filename)
    df = pd.read_csv(filename, index_col=None, header=0)
    data.append(df)
df = pd.concat(data, axis=0, ignore_index=True)

print(df)

df['MeshHeadingList'] = df.MeshHeadingList.str.lower()
dateRange = pd.date_range(start='2000',end='2020',freq="Y").year
print(dateRange)
filtered = df.loc[df['JournalPubDate'].isin(dateRange)].year.astype(str)
print(filtered)

groupedKeywords = filtered.groupby('MeshHeadingList')['JournalCountry'].count().sort_values(ascending=False).index[:10]
print(groupedKeywords)
filtered = filtered.loc[filtered['MeshHeadingList'].isin(groupedKeywords)]
filtered['num']=1
print(filtered)

keywordChanges = filtered.pivot_table('num', index='JournalPubDate',
                                columns='MeshHeadingList',aggfunc=sum).fillna(0)
print(keywordChanges)

keywordChanges.plot(title='Keyword Trend', figsize=(20,20))
plt.legend(loc='best')
plt.savefig('top30in215.png')