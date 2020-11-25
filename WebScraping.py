from bs4 import BeautifulSoup
import pandas as pd 
import requests
import urllib.request
import time 

# Create lists to store the scraped data 
print("dd")
authors = []
dates = []
statements = []
sources = []
targets = [] 

def scrape_website(page_number):


    page_num = str(page_number)  
    URL = 'https://www.politifact.com/factchecks/list/?page='+page_num 
    webpage = requests.get(URL)  
    time.sleep(3)
    soup = BeautifulSoup(webpage.text, "html.parser") 
    statement_footer =  soup.find_all('footer',attrs={'class':'m-statement__footer'}) 
    statement_quote = soup.find_all('div', attrs={'class':'m-statement__quote'}) 
    statement_meta = soup.find_all('div', attrs={'class':'m-statement__meta'})
    target = soup.find_all('div', attrs={'class':'m-statement__meter'}) 
    for i in statement_footer:
        link1 = i.text.strip()
        name_and_date = link1.split()
        first_name = name_and_date[1]
        last_name = name_and_date[2]
        full_name = first_name+' '+last_name
        month = name_and_date[4]
        day = name_and_date[5]
        year = name_and_date[6]
        date = month+' '+day+' '+year
        dates.append(date)
        authors.append(full_name)
    for i in statement_quote:
        link2 = i.find_all('a')
        statements.append(link2[0].text.strip())
    for i in statement_meta:
        link3 = i.find_all('a') 
        source_text = link3[0].text.strip()
        sources.append(source_text)
    for i in target:
        fact = i.find('div', attrs={'class':'c-image'}).find('img').get('alt')
        targets.append(fact)
n=2
for i in range(1, n):
        scrape_website(i)
data = pd.DataFrame(columns = ['author',  'statement', 'source', 'date', 'target']) 
data['author'] = authors
data['statement'] = statements
data['source'] = sources
data['date'] = dates
data['target'] = targets
print("ff")
#Create a function to get a binary number from the target
def getBinaryNumTarget(text):
  if text == 'true':
    return 1
  else:
    return 0
#Create a function to get only true or false values from the target
def getBinaryTarget(text):
  if text == 'true':
    return 'REAL'
  else:
    return 'FAKE'
#Store the data in the dataframe
data['BinaryTarget'] = data['target'].apply(getBinaryTarget)
data['BinaryNumTarget'] = data['target'].apply(getBinaryNumTarget)
print(data)
data['BinaryNumTarget']
t , f = 0 , 0 
for i in data['BinaryNumTarget'] : 
    if i == 0 : 
        f+=1
    else : 
        t+=1
print("{} fake news in {} news posted in the political website ".format(f,t))
        