import pandas as pd
import sys
import csv
from datetime import date
from tabulate import tabulate
import random

# thingstodo replay fuinction, more functions, comments

# in csv file, with n=index of column (start from 0) column 3n = finnish, 3n+1 = english, 3n+2=sentence example with
# the finnish word.

# function to print the example/description of word, to make distinction between french text and finnish sentences. 
# French description are between parenthesis
def print_example(string):
    if '(' in string or ')' in string:
        french_text = string[string.index('(') + 1: string.index(')')]
        print(f"\nEn français: '{french_text}'")
        string_remaining = string.replace('(' + french_text + ')', '')
        if string_remaining != '':
            print(f"An example of use is: {string_remaining}.")
    elif string != 'No description available':
        print(f"\nAn example of use is: {string}.")
        

def mode():
    mode_chosen = ''
    player_name = ''
    day_played = date.today()
    play_or_read = input("\nDo you want to play or read vocabulary?(play/read): ")
    while play_or_read != 'play' and play_or_read!='read':
        print("\nPlease enter 'play' or 'read' only: ")
        play_or_read = input("Do you want to play or read?(play/read): ")
    if play_or_read == 'read':
        mode_chosen += 'read'
    elif play_or_read == 'play':
        normal_or_random = input("\nDo you want to play regular or random mode?\nIn regular you choose the category, in random a random category is chosen for you\nEnter 'reg' or 'rand': ")
        while normal_or_random != 'reg' and normal_or_random!='rand':
            print("Please enter 'reg' or 'rand' only: ")
            normal_or_random = input("\nDo you want to play regular or random mode??(reg/rand): ")
        if normal_or_random == 'reg':
            mode_chosen += 'non_random'
        elif normal_or_random == 'rand':
            mode_chosen += 'random'
        ranked = input("\nDo you want to play for leaderboard?(y/n): ")
        while ranked != 'y' and ranked!='n':
            ("Please enter 'y' or 'n' only: ")
            ranked = input("\nDo you want to play for leaderboard?(y/n): ")
        if ranked == 'y':
            player_name = input("What is your name?: ")
            mode_chosen += '-ranked'
        elif ranked == 'n':
            mode_chosen += '-non_ranked'
    return mode_chosen, player_name, day_played


def select_data(mode_chosen):
    n_question = 20
    df = pd.read_csv('Vocab kappale.csv')
    chapters = (list(df))[::3]

    if mode_chosen == 'non_random-non_ranked' or mode_chosen == 'non_random-ranked' or mode_chosen == 'read':
        print("\nChapters: ")
        print("\n".join(["  |   ".join(chapters[i:i + 2]) for i in
                    range(0, len(chapters), 2)]))  # make it so that 2 chapters are printed per line
        
        chapter_chosen_index = int(input("\nWhat chapter do you choose?(Enter the chapter number) : "))
        while chapter_chosen_index not in range(1, len(chapters) + 1):
            chapter_chosen_index = int(input(f"\nPlease select 1 to {len(chapters)}: "))
        
        chapter_chosen_index = chapter_chosen_index - 1 # index start at 0 in list
        chapter_chosen = chapters[chapter_chosen_index]
        print(f"\nYou chose {chapter_chosen}!")

    elif mode_chosen == 'random-non_ranked' or mode_chosen == 'random-ranked':
        random_chapter_index = random.randint(0, len(chapters)-1)
        chapter_chosen_index = random_chapter_index
        chapter_chosen = chapters[chapter_chosen_index]
        print(f"\nThe following chapter was chosen for you!\n{chapter_chosen}")

    df = df[df.columns[3 * chapter_chosen_index:3 * chapter_chosen_index + 3]].dropna(how='all')
    df.fillna('No description available', inplace=True)
    df.columns = ['Finnish', 'English', 'Example/Description']

    if mode_chosen == 'read':
        print("\nHere is the vocabulary, happy learning!\n")
        print(tabulate(df, headers = 'keys', tablefmt = 'fancy_grid', showindex=False))

        continue_or_not = input("Do you want to continue or stop?(cont/stop) ")
        while continue_or_not != 'cont' and continue_or_not!='stop':
            print("Please enter 'cont' or 'stop' only: ")
            continue_or_not = input("\nDo you want to continue or stop?(cont/stop) ")
        sys.exit(0)
        #exit for now, later find way to play again
    

    if mode_chosen == 'non_random-non_ranked' or mode_chosen == 'random-non_ranked':
        n_question = int(input(f"\nHow many questions? (5 to {df.shape[0]}): "))

    chapter_df = df.sample(n_question)
    chapter_df.reset_index(drop=True, inplace=True)

    language_selected = input("\nDo you want to play Finnish->English(1) or English->Finnish(2)?: ")
    while language_selected != '1' and language_selected != '2':
        language_selected = input("Please select 1 or 2 only: ")
    if language_selected == '1':
        questions = chapter_df['Finnish'].tolist()
        correct_answers = chapter_df['English'].tolist()
        direction = 'Fin->Eng'
    elif language_selected == '2':
        questions = chapter_df['English'].tolist()
        correct_answers = chapter_df['Finnish'].tolist()
        direction = 'Eng->Fin'
    examples = chapter_df['Example/Description'].tolist()   

    return questions, correct_answers, examples, direction, chapter_chosen   


def quiz_game(questions, correct_answers, examples):
    num_correct = 0  # Correct answer counter
    for num, (question, correct_answer, example) in enumerate(zip(questions, correct_answers, examples), start=1):
        print(f"\n Question {num}:")
        answer = input(f"\nWhat is the translation of '{question}'?: ")
        if answer.lower() == correct_answer.lower() or answer.lower() in (correct_answer.lower()).split('+'):
            num_correct += 1
            print('\n ⭐ Correct! ⭐')
        # case when there are several translations separated by a coma. will accept any of the answers 
        elif answer in correct_answer.split(','):
            num_correct += 1
            print('\n ⭐ Correct! ⭐')
        else:
            print(f"\nNo the answer was: '{correct_answer}'!")
        # give the description if there is one
        if example != 'No description available':
            print_example(example)

    return num_correct, num


def score_player(num_correct, num_total):
    print(f"\n⭐⭐⭐ Your score is {num_correct} out of {num_total}! ⭐⭐⭐")
    score = (num_correct / num_total) * 100
    if score >= 90:
        print("\nExcellent!")
    elif 90 > score >= 70:
        print("\nNot bad! Keep studying")
    else:
        print("\nYou need to study more!!")

    return score


def leaderboard_update(player_name, chapter_chosen, direction, day_played, score, mode_chosen):
    if mode_chosen == 'non_random-ranked':
        with open('leaderboard_reg.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([player_name, chapter_chosen, direction, day_played, score])
    if mode_chosen == 'random-ranked':
        with open('leaderboard_rand.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([player_name, chapter_chosen, direction, day_played, score])


def leaderboard_check(mode_chosen):
    columns = ['Player name', 'chapter', 'direction', 'date', 'score %']
    if mode_chosen == 'non_random-ranked':
        df_leaderboard = pd.read_csv('leaderboard_reg.csv', names=columns, encoding='latin-1', index_col=0)
        print(df_leaderboard.sort_values(by=['score %'], ascending=False))
    if mode_chosen == 'random-ranked':
        df_leaderboard = pd.read_csv('leaderboard_rand.csv', names=columns, encoding='latin-1', index_col=0)
        #df_leaderboard.style.hide(axis="index")
        print(df_leaderboard.sort_values(by=['score %'], ascending=False))


if __name__ == '__main__':

    mode_chosen, player_name, day_played = mode()
    
    if mode_chosen == 'read':
        select_data(mode_chosen)
    else:
        questions, correct_answers, examples, direction, chapter_chosen = select_data(mode_chosen)

    num_correct, num = quiz_game(questions, correct_answers, examples)

    score = score_player(num_correct, num)

    if mode_chosen == 'random-ranked' or mode_chosen == 'non_random-ranked':
        leaderboard_update(player_name, chapter_chosen, direction, day_played, score, mode_chosen)
        check_leaderboard = input("Do you want to see the respective leaderboard?: ")
        if check_leaderboard == 'y':
            leaderboard_check(mode_chosen)

    #Define MODE ->
    #PLAY OR READ, if PLAY reg or rand, leaderboard or not,fi to eng or eng to fi

    #Import data and choose according to mode chosen

    #ask questions and count answers

    # print score

    #Write to leadberbord if leaderboard mode, ask to check leaderboard if wanted

    #play again or read