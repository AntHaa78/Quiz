import pandas as pd
import random
from tkinter import *

# read csv file with datas
df = pd.read_csv('Vocab chapters.csv')

# Create categories-list
categories = []
for row in df:
    categories.append(row)

# Define if vocab will be fin or eng, useful for selecting other (translated) column
category_fi = categories[::2]
category_en = categories[1::2]


def define_vocab_list():
    category_chosen = user_category_field.get()
    category_chosen = category_chosen.title()
    if category_chosen in categories:
        text = f"You've selected {category_chosen}! Let the quiz begin"
        button_confirm_category.config(text=text)

        if category_chosen in category_fi:
            vocab_chosen = df[category_chosen].tolist()
            category_chosen_translated = category_chosen.replace('Fi', 'En')
            vocab_chosen_translated = df[category_chosen_translated].tolist()
            # Remove possible nan from the empty csv cells
            vocab_chosen_cleaned = [x for x in vocab_chosen if str(x) != 'nan']
            vocab_chosen_translated_cleaned = [x for x in vocab_chosen_translated if str(x) != 'nan']

        else:
            vocab_chosen = df[category_chosen].tolist()
            category_chosen_translated = category_chosen.replace('En', 'Fi')
            vocab_chosen_translated = df[category_chosen_translated].tolist()
            # Remove possible nan from the empty csv cells
            vocab_chosen_cleaned = [x for x in vocab_chosen if str(x) != 'nan']
            vocab_chosen_translated_cleaned = [x for x in vocab_chosen_translated if str(x) != 'nan']

        # Create dict of words and translated words (questions/correct answer, easy to shuffle together for quiz)
        result = dict(zip(vocab_chosen_cleaned, vocab_chosen_translated_cleaned))
        result = random.sample(list(result.items()), k=len(result))
        questions = []
        global correct_answers
        correct_answers = []
        for question, correct_answer in result:
            questions.append(question)
            correct_answers.append(correct_answer)

        question_text = 'What is the translation of: '
        label_question1.config(text=question_text + questions[0])
        label_question2.config(text=question_text + questions[1])
        label_question3.config(text=question_text + questions[2])
        label_question4.config(text=question_text + questions[3])
        label_question5.config(text=question_text + questions[4])
    else:
        text = 'Please choose among the selected categories only!'
        button_confirm_category.config(text=text)
        root.after(4000, lambda: root.destroy())


def check_answers():
    answers = [answer1_field.get(), answer2_field.get(), answer3_field.get(), answer4_field.get(), answer5_field.get()]
    num_correct = 0
    for answer, correct_answer in zip(answers, correct_answers):
        if answer == correct_answer or answer.lower() == correct_answer or answer.title() == correct_answer:
            num_correct += 1
        elif answer in correct_answer and (',' in correct_answer):
            num_correct += 1
        else:
            pass
    button_check_answers.config(text='Your score is ' + str(num_correct) + '/5!')


def show_correct_answers():
    text = f'The correct answers are:\nQuestion1: {correct_answers[0]} | Question2: {correct_answers[1]}  \n' \
           f'Question3: {correct_answers[2]} | Question4: {correct_answers[3]} \n Question5: {correct_answers[4]} '
    button_show_correct_answers.config(text=text)


def clear_all():
    user_category_field.delete(0, END)
    button_confirm_category.config(text='Please select a category')
    button_check_answers.config(text='Check answers')
    button_show_correct_answers.config(text='Show all correct answers')
    answer1_field.delete(0, END)
    answer2_field.delete(0, END)
    answer3_field.delete(0, END)
    answer4_field.delete(0, END)
    answer5_field.delete(0, END)
    label_question1.config(text='Waiting for category...')
    label_question2.config(text='Waiting for category...')
    label_question3.config(text='Waiting for category...')
    label_question4.config(text='Waiting for category...')
    label_question5.config(text='Waiting for category...')


# Create a GUI Window
root = Tk()

# set the size of the GUI Window
root.geometry("1500x600")

# set the title of the Window
root.title("Quiz")

str_categories = 'CATEGORIES: ' + ' | '.join(categories)
label_categories = Label(root, text=str_categories, fg='red')
label_categories.grid(row=1, column=1, padx=10, pady=10)

label_user_category = Label(root, text='Please choose a chapter among the ones proposed above: ', fg='black')
label_user_category.grid(row=2, column=0, padx=10, pady=10)

user_category_field = Entry(root)
user_category_field.grid(row=2, column=2, padx=10, pady=10)

button_confirm_category = Button(root, text='Confirm category', bg='red', fg='black', command=define_vocab_list)
button_confirm_category.grid(row=3, column=1, padx=10, pady=10)

label_question1 = Label(root, text='Waiting for category...')
label_question1.grid(row=4, column=0, pady=10)

label_question2 = Label(root, text='Waiting for category...')
label_question2.grid(row=5, column=0, pady=10)

label_question3 = Label(root, text='Waiting for category...')
label_question3.grid(row=6, column=0, pady=10)

label_question4 = Label(root, text='Waiting for category...')
label_question4.grid(row=7, column=0, pady=10)

label_question5 = Label(root, text='Waiting for category...')
label_question5.grid(row=8, column=0, pady=10)

answer1_field = Entry(root)
answer1_field.grid(row=4, column=2, padx=10, pady=10)

answer2_field = Entry(root)
answer2_field.grid(row=5, column=2, padx=10, pady=10)

answer3_field = Entry(root)
answer3_field.grid(row=6, column=2, padx=10, pady=10)

answer4_field = Entry(root)
answer4_field.grid(row=7, column=2, padx=10, pady=10)

answer5_field = Entry(root)
answer5_field.grid(row=8, column=2, padx=10, pady=10)

button_check_answers = Button(root, text='Check answers', bg='red', fg='black', command=check_answers)
button_check_answers.grid(row=9, column=1, padx=10, pady=10)

button_show_correct_answers = Button(root, text='Show all correct answers', bg='red', fg='black',
                                     command=show_correct_answers)
button_show_correct_answers.grid(row=10, column=0, padx=10, pady=10)

button_clear_all = Button(root, text='Reset all', bg='red', fg='black', command=clear_all)
button_clear_all.grid(row=10, column=2, padx=10, pady=10)

root.mainloop()
