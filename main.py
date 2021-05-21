import discord
import pandas as pd
from settings import TOKEN

import mysql.connector

client = discord.Client()


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):
    try:
        from settings import mysql_cnx
        mysql_cnx.ping(reconnect=True)
        if message.author == client.user:
            return

        # trim message
        message.content.lstrip().rstrip()
        if message.content.startswith('!viki'):
            try:
                command = message.content.split(' ', 1)[1]
            except:
                print("No command, say hi!")

                # !viki
                await message.channel.send(f'Hello, {message.author}')
                return

            # !viki sql <SQL>
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

            # !viki get-all-tags
            if command.startswith('get-all-tags'):
                try:
                    sql = "SELECT tag FROM viki.info"
                    cursor = mysql_cnx.cursor()
                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    out = pd.DataFrame(rows).to_string(index=False, header=False)
                    cursor.close()
                    await message.channel.send(f"`{out[0:1998]}`")

                except Exception as e:
                    await message.channel.send(f"`{e}`")

            # !viki get-info <tag>
            if command.startswith('get-info'):
                try:
                    tag = command.split(' ', 1)[1].lstrip('"').rstrip('"')
                    sql = f"SELECT data FROM viki.info WHERE tag = '{tag}'"
                    cursor = mysql_cnx.cursor()
                    cursor.execute(sql)
                    row = cursor.fetchone()
                    cursor.close()

                    if row is None:
                        out = f"{tag} does not exist."
                    else:
                        out = row[0]

                    await message.channel.send(f"`{out}`")

                except Exception as e:
                    await message.channel.send(f"`{e}`")

            # !viki store-info <tag> <data>
            if command.startswith('store-info'):
                try:
                    tag = command.split(' ', 1)[1].split(' ')[0].lstrip('"').rstrip('"')
                    data = command.split(' ', 1)[1].split(' ', 1)[1].lstrip('"').rstrip('"')
                    sql = f"INSERT INTO viki.info (tag, data, createdBy) VALUES ('{tag}', '{data}', '{message.author}')"
                    cursor = mysql_cnx.cursor()
                    cursor.execute(sql)
                    cursor.close()
                    mysql_cnx.commit()
                    await message.channel.send(f"`{tag} has been stored successfully.`")

                except mysql.connector.IntegrityError as e:
                    await message.channel.send(f"`Error: {tag} already exists. Use update-info instead.`")

                except Exception as e:
                    await message.channel.send(f"`Error: {e}`")

        mysql_cnx.close()
    
    except:
        await message.channel.send(f"`Service unavailable.`")


client.run(TOKEN)
