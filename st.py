from collections import namedtuple
from flask import request
from flask import Flask, render_template, redirect, url_for, request
import re

import wolframalpha

city = ""
temp = ""
status = ""
pic = ""
errormsg = ''

app = Flask(__name__)

#Tmperature: ['temperature | 4 °C\nconditions | cloudy\nrelative humidity | 93% (dew point: 3 °C)\nwind speed | 1 m/s\n(43 minutes ago)']

def KnowWez(move):


    app_id = 'KWP6AY-PH9U2V5GTY'
    client = wolframalpha.Client(app_id)
    res = client.query(move + ' weather')
    if not res["@success"] == "true":
        print ("ZA RABOTOY")
        return redirect(url_for('Index'))

    else:
        answer = (res['pod'][1]['subpod']['img']['@title'])
        full = answer.split("|")
        cels_text = full[1]
        #print (cels_text)
        #cels_text.split()
        #celsium = cels_text[1]
        celsium = cels_text[:cels_text.find('C')]
        #print (celsium)
        #print (full[2])
        status_text = full[2]
        #print (status_text)
        StatRes = ''
        if re.search(r'\bsnow\b', status_text):
            StatRes = 'Snowy'
            return status_text, celsium, StatRes
        elif re.search(r'\brain\b', status_text):
            StatRes = 'Rainy'
            return status_text, celsium, StatRes
        elif re.search(r'\bcloudy\b', status_text) or re.search(r'\bovercast\b', status_text):
            StatRes = 'Cloudy'
            return status_text, celsium, StatRes
        elif re.search(r'\fog\b', status_text):
            StatRes = 'Fogy'
            return status_text, celsium, StatRes
        else:
            StatRes = '+'
            return status_text, celsium, StatRes


@app.route('/', methods = ['GET'])
def Index():
    return render_template('index.html')


@app.route('/weather', methods = ['GET'])
def Weather():
    return render_template('weather.html', city = city, temp = temp, status = status, pic = pic)

@app.route('/search', methods=['POST'])
def add_message():
    text = request.form['text']
    FullInfo = KnowWez(text)
    try:
        stat = FullInfo[0]
        stat = FullInfo[0]
        cels = FullInfo[1]
        global city
        city = text
        global temp
        temp = cels
        global status
        status = stat
        global pic
        pic = FullInfo[2]
        #print (pic)
        return redirect(url_for('Weather'))

    except:
        KeyError
        TypeError
        #print ("get back")
        global errormsg
        errormsg = "incorrect city name. try again"
        return render_template('weather.html', errormsg = errormsg)

app.debug = True
app.run()
