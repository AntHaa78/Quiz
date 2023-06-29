import requests
import pandas as pd
import json
import random
import os
from apifunction import *

#read csv file with datas
df=pd.read_csv('vocab quiz.csv')

#Create categories-list
categories=[]
for row in df:
    categories.append(row)

#Define if vocab will be fin or eng, useful for api call translate source/target (0 2 4 columns = fin)
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




#Use the translate function depending on fin/eng list chosen
if category_chosen in category_fi:
    fi_translate(vocab_chosen_cleaned)
    vocab_chosen_translated=fi_translate(vocab_chosen_cleaned)
else:
    en_translate(vocab_chosen_cleaned)
    vocab_chosen_translated = en_translate(vocab_chosen_cleaned)


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

