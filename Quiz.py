import requests
import pandas as pd
import json
import random

#read csv file with data
df=pd.read_csv('vocab quiz.csv')

#Create categories-list
categories=[]
for row in df:
    categories.append(row)

#Define if vocab will be fin/eng, useful for Api call translate (source/target)
category_fi=categories[::2]

#Ask user what category, loop if answer incorrect (not one of the categories)
while True:

    category_chosen=input(f"Choose a category: {categories}: ")
    if  category_chosen not in categories:
        print("\n Please choose among the proposed categories (don't forget upper letter)")
        continue
    else: 
        print(f"\n You've chosen {category_chosen!r}! Let the quiz begin \n")
        break


#Create the vocabulary list according to category chosen
vocab_chosen=df[category_chosen].tolist()
#Remove the nan from the empty csv cells
vocab_chosen_cleaned=[x for x in vocab_chosen if str(x) != 'nan']

#randomize the order of the vocab list
#random.shuffle(vocab_chosen_cleaned)

#word=random.choice(vocab_chosen_cleaned)


#Call the google translate api
#if category_chosen in category_fi:
    # mydata={'source':'fi', 'target':'en', 'q':vocab_chosen_cleaned}
#else:
    # mydata={'source':'en', 'target':'fi', 'q':vocab_chosen_cleaned}

#print(word)
#print(mydata)

response=requests.post("https://google-translate1.p.rapidapi.com/language/translate/v2",
    data = {'source': 'en','target': 'fi','q': vocab_chosen_cleaned},
    headers={
    'content-type': 'application/x-www-form-urlencoded',
    "Accept-Encoding": "application/gzip",
    'X-RapidAPI-Key': 'c862fff557msh04e472cb4e3799fp17d4b0jsn23ace425136a',
    'X-RapidAPI-Host': 'google-translate1.p.rapidapi.com'
  }
)

print(response.json())


#print(vocab__chosen_cleaned)

#print(type(df.tolist()))
