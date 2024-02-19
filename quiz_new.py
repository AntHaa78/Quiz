import pandas as pd
import random
import sys

#in csv file, column 3n = finnish,3n+1 = english, 3n+2=sentence example with the finnish word. n index of column start from 0. 

# read csv file with datas
df = pd.read_csv('Vocab kappale copy.csv')

# Define chapters name (columns), every three columns is a chapter 
chapters = (list(df))[::3]


#----------------------------------------------------------------------
#old version
"""
# Ask user what category. #Todo loop if answer incorrect (not one of the categories)
while True:
    print("Chapters: ")
    print("\n".join(["  |   ".join(chapters[i:i + 3]) for i in range(0, len(chapters), 3)]))
    chapter_chosen_index = int(input("\nWhat chapter do you choose?(Enter the corresponding number) : "))
    #index start at 0 in list
    chapter_chosen_index = chapter_chosen_index-1
    # english index column will be 3 times+1the index chosen in chapters (english is every 3 other columns+1)    
    english_column_index = 3 * chapter_chosen_index +1
    # example of the finnish word used in a sentence #Todo later
    #example_column_index = 3 * chapter_chosen_index + 2
    #examples = (df.iloc[:,example_column_index]).tolist()
    #examples = [x for x in examples if str(x) != 'nan']
    chapter_chosen = chapters[chapter_chosen_index]
    print(f"\nYou chose {chapter_chosen}!")
    break

#Ask Fin->eng or eng-fin
 language_selected = int(input("\nDo you want to play Finnish->English(1) or English->Finnish(2)?: "))
if language_selected==1:
    # questions will start from finnish, so 3n columns which is also chapters name
    questions = df[chapter_chosen].tolist()
    correct_answer = (df.iloc[:,english_column_index]).tolist()
elif language_selected==2:
    correct_answer = df[chapter_chosen].tolist()
    # this time question index column is 3+1
    questions = (df.iloc[:,english_column_index]).tolist()

# Remove the nan from the empty csv cells
questions = [x for x in questions if str(x) != 'nan']
correct_answer = [x for x in correct_answer if str(x) != 'nan']

# Description mode
# result = dict(zip(questions, correct_answer, examples))
# Create dict of questions and answers (easy to shuffle together for quiz)
#result = dict(zip(questions, correct_answer))

# Set number questions according to user and randomize which words are taken
#n_question = int(input(f"How many questions? (5 to {len(questions)}): "))
#questions = random.sample(list(result.items()), k=n_question)

num_correct = 0  # Correct answer counter
for num, (question, correct_answer, example) in enumerate(questions, start=1):
    print(f"\n Question {num}:")
    answer = input(f" What is the translation of {question} : ")
    # lower method to ignore case sensitivity
    if answer.lower() == correct_answer.lower():
        num_correct += 1
        print('\n ⭐ Correct! ⭐')
    # case when there are several translations
    elif answer in correct_answer.split(','):
        num_correct += 1
        print('\n ⭐ Correct! ⭐')
    else:
        print(f" No the answer was {correct_answer!r}!")
    print(f"An example of use is: {example}")

print(f"\n Your score is {num_correct} out of {num}! ") """

#----------------------------------------------------------------------------------------
#NEW

# Ask user what category. #Todo loop if answer incorrect (not one of the categories)
while True:
    print("Chapters: ")
    print("\n".join(["  |   ".join(chapters[i:i + 3]) for i in range(0, len(chapters), 3)]))
    chapter_chosen_index = int(input("\nWhat chapter do you choose?(Enter the corresponding number) : "))
    #index start at 0 in list
    chapter_chosen_index = chapter_chosen_index-1
    chapter_chosen = chapters[chapter_chosen_index]
    print(f"\nYou chose {chapter_chosen}!")
    break

# eliminate rows where all values are nan (how=all)
df = df[df.columns[3*chapter_chosen_index:3*chapter_chosen_index+3]].dropna(how='all')
# replace nan values from the description column by "no description" in case there are none
df.fillna('No description available', inplace=True)
df.columns = ['Finnish', 'English', 'Example']
n_question = int(input(f"How many questions? (5 to {df.shape[0]}): "))
A = df.sample(n_question)
#A.reset_index()
A.reset_index(drop=True, inplace=True)
print(A)
for i in range(0, df.shape[0]):
    word_question = A.at[i,'Finnish']
    correct_answer = A.at[i,'English']
    example = A.at[i,'Example']
    answer = input(f'\nWhat is the translation of {word_question}?: ')
    if answer.lower() == correct_answer.lower():
        print('\n ⭐ Correct! ⭐')
    elif answer in correct_answer.split(','):
        print('\n ⭐ Correct! ⭐')
    else:
        print(f"\nNo the answer was {correct_answer}!")
    if example!='No description available':
        print(f"An example of use is: {example}")
