import flask
from flask import redirect, url_for, request
from telethon import TelegramClient, functions, types
from asyncio import run
import asyncio
from telethon.tl.functions.contacts import ResolveUsernameRequest
from datetime import date, timedelta  
import pandas as pd
import re
import requests
import json
import os
import random
import time

app = flask.Flask(__name__)

@app.route('/')
def start():
    return str(os.path.abspath(os.curdir))
    #return('write /download to url to load excel')

@app.route('/download', methods=['GET', 'POST'])
def download():
    ran = time.time()
    channel = 'Segodnya_life'
    url = """https://api.telegram.org/bot986604365:AAHiOKpoNY3YNF71Jav26J6ONSFnDft9rJ0/getChatMemberCount?chat_id=@"""+channel
    r = requests.get(url)
    numberofusers = json.loads(r.text).get('result')
    name = 'anon'
    chat = 'Segodnya_life'
    api_id = 16865639
    api_hash = '81aacb85d2a6e578ae6584d00f18866c'
    r = re.compile("[^а-яА-Я?!,.:%;№$""0-9''\s\- ]+")
    data = {'Channel':[], 'Number of subscribers':[], 'Text': [], 'Date': [], 'Views':[], 'Forwards':[],'Pinned':[]}   
    df = pd.DataFrame(data)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    with TelegramClient(name, api_id, api_hash) as client:
        for message in client.iter_messages(chat):
            if message.date.date() != date.today():
                break
            if message.text !='':
                df.loc[len(df)] = [channel, numberofusers, r.sub('',message.text.replace('\n',' ')), str(message.date + timedelta(hours=3)), message.views, message.forwards, message.pinned]
    df.to_excel("segodnya_tg_"+str(ran)+".xlsx")
    return flask.send_file("segodnya_tg_"+str(ran)+".xlsx", as_attachment=True)

@app.route('/update')
def update():
    os.remove(os.path.abspath(os.curdir)+"/parsing_tg.xlsx")
    return redirect(url_for('download'))

if __name__ == "__main__":
    app.run()