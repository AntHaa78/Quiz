import requests
import pandas as pd
import json
import random

#read csv file with datas
df=pd.read_csv('vocab quiz.csv')

#Create categories-list
categories=[]
for row in df:
    categories.append(row)

#Define if vocab will be fin or eng, useful for api call translate (source/target)
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




#Configure my data (source/target language) then call the google translate api
if category_chosen in category_fi:
     mydata={'source':'fi', 'target':'en', 'q':vocab_chosen_cleaned}
else:
     mydata={'source':'en', 'target':'fi', 'q':vocab_chosen_cleaned}

response=requests.post("https://google-translate1.p.rapidapi.com/language/translate/v2",
    data = mydata,
    headers={
    'content-type': 'application/x-www-form-urlencoded',
    "Accept-Encoding": "application/gzip",
    'X-RapidAPI-Key': 'c862fff557msh04e472cb4e3799fp17d4b0jsn23ace425136a',
    'X-RapidAPI-Host': 'google-translate1.p.rapidapi.com'
  }
)

result=response.json()
vocab_chosen_translated=[d['translatedText'] for d in (result['data'])['translations']]

#Create dict of words and translated words (easy to shuffle together for quiz)
result=dict(zip(vocab_chosen_cleaned, vocab_chosen_translated))

#Set questions asked to 5 and randomize which words are taken
questions=random.sample(list(result.items()), k=5)

num_correct=0 # Correct answer counter
for num, (question, correct_answer) in enumerate(questions, start=1):
    print(f"\n Question {num}:")
    answer=input(f" What is the translation of {question} : ")
    if answer==correct_answer:
        num_correct+=1
        print('\n ⭐ Correct! ⭐')
    else:
        print(f" No the answer was {correct_answer!r}!")
    
print(f"\n Your score is {num_correct} out of {num}! ")

