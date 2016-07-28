"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request, response
import json
import datetime
from http import cookies
import random
from random import randint


boto_memory = {"user_name":"nouser"}
animation=['afraid','bored','confused','cry','dan','dog','excit','giggling','broke','love','funny','money']
special_words=['dan','excit','broke','love','cry','funny']
special_words_translate={'dan':'dancing','excit':'excited','broke':'heartbroke','love':'inlove','cry':'crying','funny':'laughing'}
robot={'afraid':'why so scared?',
       'love':'i love you too',
       'bored':'am i boring you?',
       'confused':'why so confused?',
       'cry':'no do not cry i love you!',
       'dan':'do you want to dance with me',
       'dog':'he looks so cute no?',
       'excited':'i am also very excited',
       'funny':'ha ha ha very funny',
       'broke':'but i love you!',
       'money':'i love money too'
       }
questions={'your name':'my name is boto','my name': 'your name is **user_name**','old you':'i am too old to tell', 'old am i':'you are **user_age**','are you':'i am fine and you',
           'do i get':'i suggest tou ask that to google maps','language you speak':'i speak english and you','you hungry':'very want to grab a bite?'}

jokes=['Can a kangaroo jump higher than a house? Of course, a house doesn’t jump at all',
       ' Anton, do you think I’m a bad mother? My name is Paul.',
       'Scientists have now discovered how women keep their secrets.They do so within groups of 40.',
       'My wife’s cooking is so bad we usually pray after our food.',
       'I cannot believe I forgot to go to the gym today. that is 7 years in a row now.',
       'What goes up and down but never moves? the stairs']
bad_words=['']
answers={"first":False}
c = cookies.SimpleCookie()

@route('/', method='GET')
def index():
    response.set_cookie('name', 'nouser')
    return template("chatbot.html")


def first_answer():
    return {"animation": "takeoff", "msg": "what an amazing name **user_name**" }

def check_for_special_word(msg):
    if msg in special_words:
        return {"animation": special_words_translate[msg], "msg": robot[msg]}
    else:
        return {"animation": msg, "msg": robot[msg]}

def time():
    time = datetime.datetime.now().time()
    return {"animation": "waiting", "msg": "it is " + str(time)}

def joke():
    ran = randint(0, len(jokes))
    return {"animation": "laughing", "msg": jokes[ran]}


def injectMemory(phrase):
    newPhrase = phrase
    for key in boto_memory:
        newPhrase = newPhrase.replace("**" + key + "**", boto_memory[key])
    return newPhrase

def handle_questions(msg):
    for question in questions:
        if question in msg:
            return {"ok": "laughing", "msg": questions[question]}
        else:
            return {"no": "laughing", "msg": 'sorry but your question is unclear please ask again'}




# //getting a message from the clien and returning it
@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    user_name = request.cookies.get('name', 'nouser')
    robotAnswer = {"animation": "giggling", "msg": "that is very funny"}
    boto_memory['user_name'] = user_message
    if user_name == "nouser":
        response.set_cookie('name', user_message)
        boto_memory['user_name'] = user_message
        robotAnswer = first_answer()
    elif '?' in user_message:
        robotAnswer=handle_questions(user_message)
    else:
        for word in animation:
            if word in user_message:
                robotAnswer = check_for_special_word(word)
            elif 'what'in user_message and 'time' in user_message:
                robotAnswer = time()
            elif 'joke' in user_message:
                robotAnswer = joke()
    robotAnswer["msg"] = injectMemory(robotAnswer["msg"])
    return json.dumps(robotAnswer)


@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)

if __name__ == '__main__':
    main()
