import requests
from tkinter import *
import random
from bs4 import BeautifulSoup

class Quiz:

    def __init__(self):
        self.question_no=0
        self.display_title()
        self.display_question()
        self.answer=self.entry_answers()
        self.buttons()
        self.data_size=len(question)
        self.correct=0

    def display_result(self):
        score = f'You have {self.correct}/{self.data_size} correct answers!'
        mb.showinfo("Result", f'{score}')

    def check_ans(self, question_no):
        if self.answer.get() == answer[question_no]:
            return True

    def choose_difficulty(self):
        if difficulty_field.get():
            url = "https://uusikielemme.fi/finnish-vocabulary"
            response = requests.get(url)
            global soup
            soup = BeautifulSoup(response.text, 'html.parser')
            links_html = soup.find_all('a')  # <a> are hyperlinks in html

            # Create difficulty categories-list
            categories = [t.text for t in links_html]
            beginner_category = categories[categories.index('Finnish loanwords'):categories.index('Liquid foods') + 1]
            intermediate_category = categories[
                                    categories.index('List of hobbies'):categories.index('100 random nouns') + 1]
            advanced_category = categories[categories.index('Government and politics'):categories.index(
                'Adjectives with fixed modifiers') + 1]
            difficulty = difficulty_field.get()
            if difficulty == 'beginner':
                categories_str = "\n".join(
                    [" | ".join(beginner_category[i:i + 10]) for i in range(0, len(beginner_category), 10)])
            elif difficulty == 'intermediate':
                categories_str = "\n".join(
                    [" | ".join(intermediate_category[i:i + 10]) for i in range(0, len(intermediate_category), 10)])
            elif difficulty == 'advanced':
                categories_str = "\n".join(
                    [" | ".join(advanced_category[i:i + 10]) for i in range(0, len(advanced_category), 10)])
            else:
                return 'Not a valid category'

    def choose_category(self):
        if category_field.get():
            category=category_field.get()
            # Access to second URL (depending on answer before) where actual finnish and english words are listed in rows
            link = soup.find('a', string=category)
            url2 = link['href']
            response2 = requests.get(url2)
            soup2 = BeautifulSoup(response2.text, 'html.parser')
            rows_html = soup2.find_all('td')

            # Define two list for finnish/english words
            finnish_words = [t.text for t in rows_html[::2]]
            english_words = [t.text for t in rows_html[1::2]]

            # Create dict of words and translated words (questions/correct answer, easy to shuffle together for quiz)
            global resultat
            resultat = dict(zip(finnish_words, english_words))
            global correct_answer_list
            correct_answer_list = list(resultat.values())