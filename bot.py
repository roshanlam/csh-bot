import discord
from discord.ext import commands
import json
from pymongo import MongoClient
import re

client = discord.Client(intents=discord.Intents.all())
filedata = {}

with open('config.json') as f:
    filedata = json.load(f)

dbclient = MongoClient(filedata['mongoURI'])
db = dbclient.test
collection = db.resources

#bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
#@bot.command()
#async def search(ctx, query):
#    await ctx.send('Query {}'.format(query))

@client.event
async def on_ready():
    print('Bot is running')

resources_and__help_channels = [
    1078868466838282320, 1078868442226106378, 1081337945975431309, 1088248576540418158,
    1078441318210080892, 1078441608653066330, 1093875172483805256, 1088248543271211069,
    1094788875370639510
]

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
        
    # if message content starts with $query then search for the query 

client.run(filedata['token'])