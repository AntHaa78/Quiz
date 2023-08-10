from tkinter import *

finnish = ['älykäs', 'nokkela', 'loistava', 'monimutkainen', 'harkittu']
english = ['intelligent', 'clever / smart', 'brilliant', 'complicated', 'premeditated, deliberate']
result = dict(zip(finnish, english))

word_to_translate = list(result.keys())
correct_answer_list = list(result.values())


def questions(num):
    return f'What is the translation of {word_to_translate[num - 1]}?'


def check_answers():
    answer1 = answer1_field.get()
    answer2 = answer2_field.get()
    answer3 = answer3_field.get()
    answer4 = answer4_field.get()
    answer5 = answer5_field.get()
    user_answer_list = [answer1, answer2, answer3, answer4, answer5]
    num_correct = 0
    for answer, correct_answer in zip(user_answer_list, correct_answer_list):
        if answer == correct_answer:
            num_correct += 1
        elif answer in correct_answer and ('/' in correct_answer or ',' in correct_answer):
            num_correct += 1
        else:
            num_correct = num_correct
    #number_correct_answers = len(set(user_answer_list) & set(correct_answer_list))
    res = f'You have {num_correct} correct answers!'
    button_check_score.config(text=res)


def clear_all():
    answer1_field.delete(0, END)
    answer2_field.delete(0, END)
    answer3_field.delete(0, END)
    answer4_field.delete(0, END)
    answer5_field.delete(0, END)


root = Tk()

root.title('Translation Quiz')
root.geometry('550x300')

label_question1 = Label(root, text=questions(1), fg='black', bg='white')
label_question2 = Label(root, text=questions(2), fg='black', bg='white')
label_question3 = Label(root, text=questions(3), fg='black', bg='white')
label_question4 = Label(root, text=questions(4), fg='black', bg='white')
label_question5 = Label(root, text=questions(5), fg='black', bg='white')

label_question1.grid(row=1, column=0, padx=10, pady=10)
label_question2.grid(row=2, column=0, padx=10, pady=10)
label_question3.grid(row=3, column=0, padx=10, pady=10)
label_question4.grid(row=4, column=0, padx=10, pady=10)
label_question5.grid(row=5, column=0, padx=10, pady=10)

answer1_field = Entry(root)
answer2_field = Entry(root)
answer3_field = Entry(root)
answer4_field = Entry(root)
answer5_field = Entry(root)

answer1_field.grid(row=1, column=1, padx=10, pady=10)
answer2_field.grid(row=2, column=1, padx=10, pady=10)
answer3_field.grid(row=3, column=1, padx=10, pady=10)
answer4_field.grid(row=4, column=1, padx=10, pady=10)
answer5_field.grid(row=5, column=1, padx=10, pady=10)

button_check_score = Button(root, text='Submit answers and display score', bg='red', fg='black', command=check_answers)
button_check_score.grid(row=6, column=0, padx=10, pady=10)

button_clear_all = Button(root, text='Clear all', command=clear_all)
button_clear_all.grid(row=6, column=1, padx=10, pady=10)

root.mainloop()
