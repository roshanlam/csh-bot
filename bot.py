import asyncio
import traceback
import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context
from discord import app_commands
import json
from pymongo import MongoClient
import re
import requests
from modal import Modal

client = discord.Client(intents=discord.Intents.all())
filedata = {}

with open('config.json') as f:
    filedata = json.load(f)

dbclient = MongoClient(filedata['mongoURI'])
db = dbclient.test
collection = db.resources
bot = Bot(command_prefix='!', intents=discord.Intents.all())


@client.event
async def on_ready():
    print('Bot is running')

resources_and__help_channels = [
    1078868466838282320, 1078868442226106378, 1081337945975431309, 1088248576540418158,
    1078441318210080892, 1078441608653066330, 1093875172483805256, 1088248543271211069,
    1094788875370639510
]

def calcGrade(grades: dict):
    with open('gradeCalc.json') as f:
        data = json.load(f)
    grade = 0
    for key in data:
        if key == grades['class']:
            data = data[key]
            break
    for key in grades:
        if key == 'class':
            continue
        grade += float(grades[key]) * (data[key]/100)
    return grade


def getJoke():
    content = requests.get('https://v2.jokeapi.dev/joke/Any?', headers={'Accept': 'application/json'}).json()
    if content['type'] == 'single':
        return content['joke']
    elif content['type'] == 'twopart':
        return content['setup'] + '\n' + content['delivery']

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == 'hello':
        await message.channel.send('Hello {}'.format(message.author))
        
    if message.channel.id in resources_and__help_channels:
        url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        urls = url_pattern.findall(message.content)
        data = {
            "message": message.content,
            "urls": urls
        }
        collection.insert_one(data)

    if message.content == '!grades':
        grades = collection.find_one({"user": message.author.id})
        if grades:
            grade = calcGrade(grades)
            await message.channel.send(f'Your grade is {grade}')
        else:
            await message.channel.send('No grades found')
    
    if message.content == '!joke':
        joke = getJoke()
        await message.channel.send(joke)
    
    

client.run(filedata['token'])
