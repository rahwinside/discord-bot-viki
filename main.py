import discord
import pandas as pd
from settings import TOKEN, mysql_cnx

client = discord.Client()


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # trim message
    message.content.lstrip().rstrip()
    if message.content.startswith('!viki'):
        try:
            command = message.content.split(' ', 1)[1]
        except:
            print("No command, say hi!")
            await message.channel.send(f'Hello, {message.author}')
            return

        if command.startswith('sql'):
            try:
                sql = command.split(' ', 1)[1]
                cursor = mysql_cnx.cursor()
                cursor.execute(sql)
                rows = cursor.fetchall()
                fields = [i[0] for i in cursor.description]
                out = pd.DataFrame(rows, columns=fields)
                cursor.close()
                await message.channel.send(f"`{str(out)[0:1998]}`")
            except Exception as e:
                await message.channel.send(f"`{e}`")


client.run(TOKEN)
