import discord
from settings import TOKEN
from mysql_config import cnx

client = discord.Client()

@client.event
async def on_ready():
  print(f"Logged in as {client.user}")


@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if message.content.startswith('!viki'):
    command = message.content.split(' ', 1)[1]
    if len(command) == 0:
      await message.channel.send(f'Hello, {message.author}')
    if command.startswith('sql'):
      try:
        sql = command.split(' ', 1)[1]
        cursor = cnx.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        await message.channel.send(f"`{str(rows)[0:1998]}`")
      except Exception as e:
        await message.channel.send(f"`{e}`")


client.run(TOKEN)
