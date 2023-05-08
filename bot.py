import discord
from discord.ext.commands import Bot, Context
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


def getJoke(query=None):
    if query is None:
        content = requests.get('https://v2.jokeapi.dev/joke/Any?', headers={'Accept': 'application/json'}).json()
        if content['type'] == 'single':
            return content['joke']
        elif content['type'] == 'twopart':
            return content['setup'] + '\n' + content['delivery']
    else:
        content = requests.get('https://v2.jokeapi.dev/joke/Any?contains={}'.format(query), headers={'Accept': 'application/json'}).json()
        if content['type'] == 'single':
            return content['joke']
        elif content['type'] == 'twopart':
            return content['setup'] + '\n' + content['delivery']
        
def getMeme():
    meme = requests.get('https://meme-api.com/gimme/memes/1').json()
    meme = meme['memes'][0]['url']
    return meme

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
    
    if message.content.startswith('!joke'):
        channelId = "1104254807428046939"
        if message.channel.id == int(channelId):
            query = None
            args = message.content.split()[1:]
            if args:
                query = ",".join(args)
            joke = getJoke(query)
            await message.channel.send(joke)
        else:
            await message.channel.send('You can only use this command in <#{}>'.format(channelId))
        
    if message.content.startswith('!meme'):
        channelIdMeme = "1076335073487507517"
        if message.channel.id == int(channelIdMeme):
            meme = getMeme()
            await message.channel.send(meme)
        else:
            await message.channel.send('You can only use this command in <#{}>'.format(channelIdMeme))

    if message.content == '!help':
        commands = []
        with open('commands.json') as f:
            commands = json.load(f)
        help_content = commands['commands']
        embed = discord.Embed(title="Help", description="Here are the commands", color=0x59b3d8)
        for key in help_content:
            embed.add_field(name=key, value=help_content[key], inline=False)
        await message.channel.send(embed=embed)
    

client.run(filedata['token'])
