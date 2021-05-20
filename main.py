import discord
import os

client = discord.Client()

@client.event
async def on_ready():
  print(f"Logged in as {client.user}")


@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if message.content.startswith('!viki'):
    await message.channel.send(f'Hello, {message.author}')

client.run(os.environ['TOKEN'])
