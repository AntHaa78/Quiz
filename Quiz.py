import pandas as pd
import sys
import csv

#todo add more leaderboard options. make functions. add comments

#in csv file, with n=index of column (start from 0) column 3n = finnish, 3n+1 = english, 3n+2=sentence example with the finnish word. 

# function to print the example/description of word, to make distinction between french text and finnish sentences
def print_example(string):
    if '(' in string or ')' in string:
        french_text = string[string.index('(')+1: string.index(')')]
        print(f"\nEn français: '{french_text}'")
        string_remaining = string.replace('('+french_text+')','')
        if string_remaining != '':
            print(f"An example of use is: {string_remaining}.")
    elif string != 'No description available':
        print(f"\nAn example of use is: {string}.")


ranked = input("Do you want to play for leaderboard?(y/n): ")
if ranked == 'y':
    player_name = input("What is your name?: ")

# read csv file with datas
df = pd.read_csv('Vocab kappale.csv')

# Define chapters name list (headers), every three columns is a chapter name
chapters = (list(df))[::3]

# Ask user what chapter.  loop if answer not within choices
print("\nChapters: ")
print("\n".join(["  |   ".join(chapters[i:i + 2]) for i in range(0, len(chapters), 2)])) # make it so that 2 chapters are printed per line
chapter_chosen_index = int(input("\nWhat chapter do you choose?(Enter the chapter number) : "))
while chapter_chosen_index not in range(1,len(chapters)+1):
    chapter_chosen_index = int(input(f"\nPlease select 1 to {len(chapters)}: "))
#index start at 0 in list
chapter_chosen_index = chapter_chosen_index-1
chapter_chosen = chapters[chapter_chosen_index]
print(f"\nYou chose {chapter_chosen}!")


# take the 3 corresponding columns and eliminate rows where all values are nan (how=all)
df = df[df.columns[3*chapter_chosen_index:3*chapter_chosen_index+3]].dropna(how='all')
# replace nan values from the description column by "no description available" in case there is none
df.fillna('No description available', inplace=True)
df.columns = ['Finnish', 'English', 'Example']

# ask user how many questions, shuffle the series together and reset the index to be clean for quiz loop. If ranked 20 questions
if ranked == 'y':
    n_question = 20
else:
    n_question = int(input(f"\nHow many questions? (5 to {df.shape[0]}): "))
chapter_df = df.sample(n_question)
chapter_df.reset_index(drop=True, inplace=True)

#Ask Fin->eng or eng-fin and make list of questions/correct answers accordingly. Save translation direction for leaderboard
language_selected = input("\nDo you want to play Finnish->English(1) or English->Finnish(2)?: ")
while language_selected!='1' and language_selected!='2':
    language_selected = input("Please select 1 or 2 only: ")
if language_selected=='1':
    questions = chapter_df['Finnish'].tolist()
    correct_answers = chapter_df['English'].tolist()
    direction = 'Fin->Eng'
elif language_selected=='2':
    questions = chapter_df['English'].tolist()
    correct_answers = chapter_df['Finnish'].tolist()
    direction = 'Eng->Fin'
examples = chapter_df['Example'].tolist()

num_correct = 0  # Correct answer counter
for num, (question, correct_answer, example) in enumerate(zip(questions, correct_answers, examples), start =1):
    print(f"\n Question {num}:")
    answer = input(f"\nWhat is the translation of '{question}'?: ")
    if answer.lower() == correct_answer.lower():
        num_correct += 1
        print('\n ⭐ Correct! ⭐')
    # case when there are several translations separated by a coma. will accept any of the answers 
    elif answer in correct_answer.split(','):
        num_correct += 1
        print('\n ⭐ Correct! ⭐')
    else:
        print(f"\nNo the answer was: '{correct_answer}'!")
    # give the description if there is one
    if example!='No description available':
        print_example(example)

print(f"\n⭐⭐⭐ Your score is {num_correct} out of {num}! ⭐⭐⭐")
score = (num_correct/num)*100
if score>=90:
    print("\nExcellent!")
elif score<90 and score>=70:
    print("\nNot bad! Keep studying")
else :
    print("\nYou need to study more!!")

if ranked == 'y':
    with open('leaderboard.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([player_name, chapter_chosen, direction, score])

leaderboard_display = input("Do you want to see the leaderboard?: ")
if leaderboard_display=='y':
    columns = ['Player name', 'chapter', 'direction', 'score %']
    df_leaderboard=pd.read_csv('leaderboard.csv', names=columns, encoding='latin-1')
    print(df_leaderboard)