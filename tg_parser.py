from telethon import TelegramClient, functions, types
from asyncio import run
from telethon.tl.functions.contacts import ResolveUsernameRequest
from datetime import date
import pandas as pd
import re
import requests
import json

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

with TelegramClient(name, api_id, api_hash) as client:
    for message in client.iter_messages(chat):
        if message.date.date() != date.today():
            break
        if message.text !='':
            df.loc[len(df)] = [channel, numberofusers, r.sub('',message.text.replace('\n',' ')), str(message.date), message.views, message.forwards, message.pinned]
    print(df)
    df.to_excel("parsing_tg.xlsx")