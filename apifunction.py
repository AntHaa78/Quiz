import os
import requests



def en_translate(words):
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv('api_key')

    response=requests.post("https://google-translate1.p.rapidapi.com/language/translate/v2",
        data = {'source':'en', 'target':'fi', 'q':words},
        headers={
        'content-type': 'application/x-www-form-urlencoded',
        "Accept-Encoding": "application/gzip",
        'X-RapidAPI-Key': api_key,
        'X-RapidAPI-Host': 'google-translate1.p.rapidapi.com'
        }
    )
    result=response.json()
    vocab_chosen_translated=[d['translatedText'] for d in (result['data'])['translations']]
    print(vocab_chosen_translated)

def fi_translate(sanat):
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv('api_key')

    response=requests.post("https://google-translate1.p.rapidapi.com/language/translate/v2",
        data = {'source':'fi', 'target':'en', 'q':sanat},
        headers={
        'content-type': 'application/x-www-form-urlencoded',
        "Accept-Encoding": "application/gzip",
        'X-RapidAPI-Key': api_key,
        'X-RapidAPI-Host': 'google-translate1.p.rapidapi.com'
        }
    )
    result=response.json()
    #vocab_chosen_translated=[d['translatedText'] for d in (result['data'])['translations']]
    #return vocab_chosen_translated
    return  [d['translatedText'] for d in (result['data'])['translations']]
    #print(vocab_chosen_translated)



#list=["car", "boat", "plane"]
#en_translate(list)