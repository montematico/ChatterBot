import discord
import time
import json
import logging
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
print("test")
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
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter',
        'chatterbot.logic.BestMatch'
    ],
    database_uri='sqlite:///database.db'
)

trainer = ChatterBotCorpusTrainer(chatbot)

trainer.train('chatterbot.corpus.english')


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

    if message.channel.name == "daryylsvoice":
        await message.channel.send(chatbot.get_response(message.content))
        print(message.content)

    if message.content.startswith('^'):
        await message.channel.send(chatbot.get_response(message.content[1:]))
        print(message.content[1:])

    if True: #set this to true to make it learn from all other channels but not respond
        response = chatbot.get_response(message.content)
        if False: #set this to true to make it respond to messages in all channels
            message.channel.send(response)

client.run(config["token"])

