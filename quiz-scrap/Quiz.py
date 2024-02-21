import random
import requests
from bs4 import BeautifulSoup

# First url to get the categories, read the html
url = "https://uusikielemme.fi/finnish-vocabulary"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
links_html = soup.find_all('a')

# Create categories-list
categories = [t.text for t in links_html]
beginner_category = categories[categories.index('Finnish loanwords'):categories.index('Liquid foods') + 1]
intermediate_category = categories[categories.index('List of hobbies'):categories.index('100 random nouns') + 1]
advanced_category = categories[
                    categories.index('Government and politics'):categories.index('Adjectives with fixed modifiers') + 1]

# Ask user what category, loop if answer incorrect (not one of the categories)
while True:
    difficulty = input("Choose a level: beginner    intermediate    advanced: ")
    if difficulty == "beginner":
        print("Categories: ")
        print("\n".join([" | ".join(beginner_category[i:i + 10]) for i in range(0, len(beginner_category), 10)]))
        category = input(f"\n Whats is your selected category: ")
        break
    elif difficulty == "intermediate":
        print(
            "\n".join([" | ".join(intermediate_category[i:i + 10]) for i in range(0, len(intermediate_category), 10)]))
        category = input(f"\n Whats is your selected category: ")
        break
    elif difficulty == "advanced":
        print("\n".join([" | ".join(advanced_category[i:i + 10]) for i in range(0, len(advanced_category), 10)]))
        category = input(f"\n Whats is your selected category: ")
        break
    else:
        print("Please select only among the 3 levels")
        category = ''
        continue

while True:
    if category not in categories:
        category = input("\nIt seems you did not type the category correctly, please rectify: ")
        continue
    else:
        print(f"\nYou selected {category}!")
        break

# Access to second URL (depending on answer before) where actual finnish and english words are listed in rows
link = soup.find('a', string=category)
url2 = link['href']
response2 = requests.get(url2)
soup2 = BeautifulSoup(response2.text, 'html.parser')
rows_html = soup2.find_all('td')

# Define two list for finnish/english words
finnish_words = [t.text for t in rows_html[::2]]
english_words = [t.text for t in rows_html[1::2]]

# Remove elements that have more than one whitespace in the finnish_words list(often are whole sentences) and the
# corresponding element in the english word list - Example Fruit category in beginner
new_finnish_words = [i for i in finnish_words if not i.count(' ') > 1]
new_english_words = [j for i, j in zip(finnish_words, english_words) if not i.count(' ') > 1]

# Create dict of words and translated words (questions/correct answer, easy to shuffle together for quiz)
result = dict(zip(new_finnish_words, new_english_words))

# Set questions to 5 and randomize which words are taken
questions = random.sample(list(result.items()), k=5)

num_correct = 0  # Correct answer counter
for num, (question, correct_answer) in enumerate(questions, start=1):
    print(f"\n Question {num}:")
    answer = input(f" What is the translation of {question} : ")
    if answer == correct_answer:
        num_correct += 1
        print('\n ⭐ Correct! ⭐')
    # Sometimes 2 translations are given, so far always separated by a comma or slash
    elif answer in correct_answer and ('/' in correct_answer or ',' in correct_answer):
        num_correct += 1
        print('\n ⭐ Correct! ⭐')
    else:
        print(f" No the answer was {correct_answer!r}!")

print(f"\n Your score is {num_correct} out of {num}! ")
