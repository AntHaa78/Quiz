from tkinter import *


result = {'käsi': 'hand', 'hammas':'tooth', 'hiukset':'hair'}

user_answer_list = []
correct_answer_list = list(result.values())

def questions(num):
    word_to_translate = list(result.keys())[num-1]
    question = f'What is the translation of {word_to_translate}?: '
    return question

def check_answers():
    answer1 = answer1_field.get()
    answer2 = answer2_field.get()
    answer3 = answer3_field.get()
    user_answer_list = [answer1, answer2, answer3]
    number_correct_answers = len(set(user_answer_list) & set(correct_answer_list))
    res = (f'You have {number_correct_answers} correct answers!')
    button1.config(text=res)


def clear_all():
    answer1_field.delete(0, END)
    answer2_field.delete(0, END)
    answer3_field.delete(0, END)

if __name__ == "__main__" :

    root = Tk()

    root.title('Translation Quiz')
    root.geometry('450x300')

    label1 = Label(root, text= questions(1), fg='black', bg='white')
    label2 = Label(root, text= questions(2), fg='black', bg='white')
    label3 = Label(root, text= questions(3), fg='black', bg='white')


    label1.grid(row=1, column=0, padx = 10, pady = 10)
    label2.grid(row=2, column=0, padx=10, pady=10)
    label3.grid(row=3, column=0, padx=10, pady=10)

    answer1_field=Entry(root)
    answer2_field=Entry(root)
    answer3_field=Entry(root)

    answer1_field.grid(row=1, column=1, padx=10, pady=10)
    answer2_field.grid(row=2, column=1, padx=10, pady=10)
    answer3_field.grid(row=3, column=1, padx=10, pady=10)





    # Create check, reset button and display score
    button1= Button(root, text='Submit answers and display score', bg='red', fg='black', command=check_answers)
    button1.grid(row=4, column=0, pady=10)
    button2= Button(root, text='Clear all', bg='red', fg='black', command=clear_all)
    button2.grid(row=5, column=1, pady=10)

    root.mainloop()
