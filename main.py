#! /usr/local/bin/python3

import discord
import time
import json
import logging
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from tendo import singleton


#make sure that there is only a single instance running
me = singleton.SingleInstance()

# read file
with open('config.json', 'r') as myfile:
    data=myfile.read()
# parse file
config = json.loads(data)

print(config["name"] + "Starting V" + config["version"])

loadtime = time.time()
client = discord.Client()
chatbot = ChatBot(
    config["name"],
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    logic_adapters=[
        #'chatterbot.logic.MathematicalEvaluation',
        #'chatterbot.logic.TimeLogicAdapter',
        'chatterbot.logic.BestMatch'
    ],
    database_uri='mongodb://localhost:27017/chatterbot-database'
)

trainer = ChatterBotCorpusTrainer(chatbot)

trainer.train('chatterbot.corpus.english')

async def timeOutChecker():
    timeout = time.time()
    time.sleep(1)
    while (timoeout - time.time()) < 180:
        #while the total time spend executing is less than 3 min. wait in the loop.
        pass

@client.event
async def on_ready():
    print('Darryl is online {0.user}'.format(client))
    print('loaded in: ' + str(round((time.time() - loadtime),2)) + 's')



@client.event
async def on_message(message):
    print(message.channel)
    print("Generating Response...")
    if message.author == client.user:
        return
    elif message.channel.name == "daryylsvoice":
        try:
            await message.channel.send(chatbot.get_response(message.content))
            print(message.content)
        except:
            return
    elif message.content.startswith('^'):
        try:
            await message.channel.send(chatbot.get_response(message.content[1:]))
            print(message.content[1:])
        except:
            return

    #commnet to make it learn from all other channels but not respond
    response = chatbot.get_response(message.content)
    message.channel.send(response)

client.run(config["token"])

