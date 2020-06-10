import discord
import time
import json
import logging
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

loadtime = time.time()
#Should get rid of some annoying errors (by ignoring them)
logger = logging.getLogger() 
logger.setLevel(logging.CRITICAL)

# reads config.json file where env variables are stored
#token, channelname, prefix, etc
with open('config.json', 'r') as myfile:
    data=myfile.read()
# parse file
config = json.loads(data)
client = discord.Client()
chatbot = ChatBot(
    config["name"],
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    #storage_adapter="chatterbot.storage.MongoDatabaseAdapter",
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter',
        'chatterbot.logic.BestMatch'
    ],
    #database_uri='mongodb://localhost:27017/chatterbot-database'
    database_uri='sqlite:///database.db'
)

trainer = ChatterBotCorpusTrainer(chatbot)

trainer.train('chatterbot.corpus.english')

@client.event
async def on_ready(): #triggers once the client is ready to do shit
    print('Darryl is online {0.user}'.format(client))
    print('loaded in: ' + str(round((time.time() - loadtime),2)) + 's') #prints how long bot took to load Chatterbot library and how long it took to connect to discord's API
    del loadtime #deletes loadtime variable since its unused to clear up memory

@client.event
async def on_message(message):
    responsetime = time.time() #starts a timer to see how long response generation takes
    if message.author == client.user:
        return #aborts response generation when message is from the bot
    elif message.channel.name == config["channel"]:
        await message.channel.send(chatbot.get_response(message.content))
        print('Generated Response in: ' + str(round((time.time() - loadtime),2)) + 's') #logs how long response generation took
    elif message.content.startswith(config["prefix"]):
        await message.channel.send(chatbot.get_response(message.content[1:])) #slices the first character from a prefix called message since otherwise in the future it may lead to generated responses including the prefix
        print('Generated Response in: ' + str(round((time.time() - loadtime),2)) + 's') #logs how long response generation took
    else:
        return #idk man, it shouldn't even get here, but if it does I don't wan't it crashing
        print('I don\'t know how but it got to the else')

    if False: #set this to true to make it learn from all other channels but not respond
        #use this if you wan't to train the bot quickly
        #note this makes it much slower and you have to be sure that whatevers hosting this can keep up.
        response = chatbot.get_response(message.content)
        if False: #set this to true to make it respond to messages in all channels
            message.channel.send(response) #I cannot stress how bad of an idea this is. Not only will you melt whatever's running this you will also most likely piss off everyone in the server since every message is responded to.

async def input("") == "exit()":
    sys.exit();

client.run(config["token"]) #it's the token used to login I don't know what you want.
#Dont Accidently Dox your bot twice by uploading the token to github.