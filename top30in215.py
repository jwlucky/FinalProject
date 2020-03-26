# import packages
import pandas as pd
import glob
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf

import wordcloud
'exec(matplotlib inline)'


# read multiple data sources
path = r'/home/output' 
all_files = glob.glob(path + "/*.csv")
li = []


for filename in all_files:
    data = pd.read_csv(filename, lineterminator='\n').drop(columns='Unnamed: 0')
    data = data[data.PMID!="PMID"]
    data['KeywordList'] = data.KeywordList.str.lower()
    data["DateCompleted"]=data.DateCompleted.str.strip(" ")
    li.append(data)

df = pd.concat(li, axis=0, ignore_index=True)

print(df)
groupedKeywords = df.groupby('KeywordList')['JournalCountry'].count().sort_values(ascending=False).index[:30]
print(groupedKeywords)
filtered = df.loc[df['KeywordList'].isin(groupedKeywords)]
filtered['num']=1
print(filtered)

keywordChanges = filtered.pivot_table('num', index='DateCompleted',
                                columns='KeywordList',aggfunc=sum).fillna(0)
print(keywordChanges)

keywordChanges.plot(title='Keyword Trend', figsize=(20,20))
plt.legend(loc='best')
plt.savefig('top30in215.png')


