import discord
import json
from chatterbot import ChatBot



client = discord.Client()
chatbot = ChatBot(
    'Daryyl',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter',
        'chatterbot.logic.BestMatch'
    ],
    database_uri='sqlite:///database.db'
)

#trainer = ListTrainer(chatbot)


@client.event
async def on_ready():
    print('Darryl is online {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user or message.author.role.name == "Bot":
        return
    if message.content.startswith('^'):
        await message.channel.send(chatbot.get_response(message.content))

client.run("Njk3MjQzODYwMzIwOTExNDg0.Xo0dWw.ATljk0W2XTr4J8rpjk9VRg4693Y")
