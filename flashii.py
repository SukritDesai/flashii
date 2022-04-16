import os
import discord
from dotenv import load_dotenv
import random
import requests
import re

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

insults = open('insults.txt', 'r').readlines()
insults = [insult.strip() for insult in insults]

people = [" - Your Mother", " - Your Best Friend", " - Guy from grocery store", " - Your dad who left 10 years ago", " - Your Grandma", " - Joe Biden", " - Barack Obama", " - Abraham Lincoln"]

def get_quote():
	response = requests.get("https://evilinsult.com/generate_insult.php?lang=en&type=text")
	return response.text + people[random.randint(0, len(people) - 1)]

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

channel_busy = False
session_permission = 'e'
people_in_session = []
cards = {}

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	if message.content.startswith('$compliment'):
		await message.channel.send('You are a ' + insults[random.randint(0, len(insults) - 1)])

	elif message.content.startswith('$quote'):
		quote = get_quote()
		await message.channel.send(quote)

	elif message.content.startswith("$start"):
		global channel_busy
		global people_in_session
		global session_permission
		if channel_busy == True:
			await message.channel.send("Channel busy cannot start another session")
		else:
			await message.channel.send('Valid Commands: $i join or $init join')

			if len(message.content) > 6 and message.content[7] == 'n':
				channel_busy = True
				session_permission = 'n'
				people_in_session.append(client.get_user(message.author.id))
				await message.channel.send(people_in_session)

			elif len(message.content) > 6 and message.content[7] == 'e':
				channel_busy = True
			else:
				await message.channel.send("Not a valid permission, enter either n or e")

	elif message.content == '$i join' or message.content == '$init join':
		uid = message.author.id
		if f"<@{uid}>" in people_in_session:
			await message.channel.send("You have already joined the session")
		if channel_busy == True and f"<@{uid}>" not in people_in_session:
			people_in_session.append(f"<@{uid}>")
			await message.channel.send(people_in_session)
		elif channel_busy == False:
			await message.channel.send("Channel not in session, cannot join.")

	elif message.content == '$end':
		channel_busy = False
		people_in_session = []
		await message.channel.send("Session has been ended")

	elif message.content.startswith('$make card'):
		make_card(message)

	elif message.content.startswith("=qa"):
		pass

@client.event
async def make_card(message):
	if channel_busy == False:
		await message.channel.send('No session. Start a session using $start -args to make cards.')
	else:
		if f'<@{message.author.id}>'in people_in_session:
			await message.channel.send("Please enter a question and answer, using =qa\nThe syntax for =qa is to add a question with Q: and add its answer with A: (in one message, it won't work otherwise)")

		else:
			await message.channel.send('You are not in the session. Join using $i join to make a card.')

client.run(TOKEN)