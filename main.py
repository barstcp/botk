#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
from flask_cors import CORS
import json

import io
import random
import string
import warnings
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import BlanklineTokenizer
import warnings
warnings.filterwarnings('ignore')

import nltk
from nltk.stem import WordNetLemmatizer
from natasha import NamesExtractor



from random import randint
import requests
extractor = NamesExtractor()


app = Flask(__name__)
CORS(app)


nltk.download('popular', quiet=True) # for downloading packages
#bot = telebot.TeleBot('1081485456:AAESvhx7lHpQ2dQIFViyE7Vbrnybk9TQ5tY')

#nltk.download('punkt') # first-time use only
#nltk.download('wordnet') # first-time use only

print("text start")
with open('text.txt') as fin:
    raw = fin.read().decode('utf-8').lower().splitlines()

with open('text.txt') as fin:
    raw1 = fin.read().decode('utf-8').lower()

print("text end")
sent_tokens = raw
word_tokens = nltk.word_tokenize(raw1)

#apihelper.proxy = {'https':'https://118.174.232.60:34772'
                           #''}

lemmer = WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

GREETING_INPUTS = ['привет'.decode('utf-8'), 'хай'.decode('utf-8'), 'здравствуйте'.decode('utf-8')]

GREETING_INPUTS_ACCOUNT = ['счет'.decode('utf-8'), 'баланс'.decode('utf-8'), 'рублей'.decode('utf-8')]


GREETING_RESPONSES = ['добрый день', 'привет', 'хай', 'здравствуйте']

def greeting(sentence):
    for word in sentence.split():
        print ('---------')
        print(word.lower())
        print ('--------')
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)
def greAccount(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS_ACCOUNT:
            return True


def response(user_response):
    response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)

    vals = cosine_similarity(tfidf[-1], tfidf)

    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()

    req_tfidf = flat[-2]

    sent_tokens.remove(user_response)

    if(req_tfidf==0):
        response= response + "Прости, я не знаю"
        print(response)

    else:
        response = response+sent_tokens[idx]

    return response

# print("start")
# @bot.message_handler(commands=['start'])
# def start_message(message):
#     print(message)
#     bot.send_message(message.chat.id, 'Привет, поговори со мной')
#
# @bot.message_handler(content_types=['text'])
# def send_text(message):
#     user_response = message.text.lower()
#     if (user_response != 'пока'):
#         if (user_response == 'спасибо'):
#             bot.send_message(message.chat.id, 'Пожалуйста, обращайтесь ')
#         else:
#             if (greeting(user_response) != None):
#                 bot.send_message(message.chat.id, greeting(user_response))
#             else:
#                 bot.send_message(message.chat.id, response(user_response))
#                 print(response(user_response))



# bot.polling()


@app.route("/api/message")
def message():
   message = request.args.get('text')
   answer = None
   user_response_account = message
   user_response = message.lower()

   if (user_response != 'пока'):
       if (user_response == 'спасибо'):
           #bot.send_message(message.chat.id, 'Пожалуйста, обращайтесь ')
           answer = 'Пожалуйста, обращайтесь'
       else:
           if (greeting(user_response) != None):
               #bot.send_message(message.chat.id, greeting(user_response))
               answer = greeting(user_response)
           elif (greAccount(user_response) == True):
               answer = 'Уточните пожалуйста ваше имя и фамилию'
           else:
               #bot.send_message(message.chat.id, response(user_response))
               text = user_response_account
               print (text)
               answer = "К сожалению вас не нашли в базу"
               matches = extractor(text)
               for match in matches:
                   start, stop = match.span
                   print(text[start:stop])
                   print ("tt")
                   test = text[start:stop]
                   if(test.encode('utf-8')== "Петр Петров"):
                       answer = "На вашем счету 100 рублей"
                   return jsonify({
                       "answer": answer
                   })

               answer = response(user_response)
               #print(response(user_response))
               #sent_tokens.remove(user_response)
   print(answer)
   #return answer

   return jsonify({
       "answer": answer
   })


@app.route("/api/upload_csv", methods=['POST'])
def upload_csv():
    # work with csv
    return jsonify({
        "type": "ok"
    })

if __name__ == '__main__':
    app.run()
    print("Server listening on port 5000")
