import discord
import json
import os
import random
import requests
import sys

from bs4 import BeautifulSoup
from datetime import timedelta
from os import environ

on_heroku = False
print(os.environ)

if not os.path.exists('config.json'):
    try:
        with open('config.json', 'w+') as f:
            json.dump({'token': 'null'}, f, indent=4, sort_keys=True)
    except Exception as e:
        print(e)

with open('config.json', 'r+') as f:
    configFile = json.load(f)

if len(sys.argv) == 2:
    token = sys.argv[1]
    configFile['token'] = sys.argv[1]

    with open('config.json', 'r+') as f:
        json.dump(configFile, f, indent=4, sort_keys=True)
else:
    token = configFile['token']
    if token == 'null':
        print('Token not configured')
        sys.exit()

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    try:
        args = message.content.split(' ')

        if message.author == client.user:
            return

        if message.content.startswith('u!help'):
            await message.channel.send('ToDo')

        elif message.content.startswith('u!about'):
            await message.channel.send('https://github.com/JoshuaVarga/Umbrellabot')

        elif message.content.startswith('u!set'):
            if message.author.guild_permissions.administrator:
                match args[1]:
                    case 'outputChannelID':
                        configFile['outputChannelID'] = args[2]
                        with open('config.json', 'r+') as f:
                            json.dump(configFile, f, indent=4, sort_keys=True)
                    case 'pingRoleID':
                        configFile['pingRoleID'] = args[2]
                        with open('config.json', 'r+') as f:
                            json.dump(configFile, f, indent=4, sort_keys=True)
                    case 'guildID':
                        configFile['guildID'] = args[2]
                        with open('config.json', 'r+') as f:
                            json.dump(configFile, f, indent=4, sort_keys=True)

            else:
                await message.channel.send('Insufficient privledges')

        elif message.content.startswith('u!game'):

            if int(args[2]) < 2 or int(args[2]) > float('inf'):
                raise Exception('Invalid range')

            def rnd(): return random.randint(0, 255)

            embed = discord.Embed(
                type='rich',
                title='Needs {} people to play {}!'.format(args[2], args[1]),
                description='If you want to play react with: ✅\nOtherwise react with: ❌',
                color=int('0x%02X%02X%02X' % (rnd(), rnd(), rnd()), 16),
                timestamp=message.created_at + timedelta(minutes=int(args[3]))
            )

            embed.set_author(name=message.author.display_name)
            embed.set_footer(text="We're playing")
            embed.set_image(url=getCoverArt(args[1]))
            embed.set_thumbnail(url=message.author.avatar_url)

            reply = await client.get_channel(int(configFile['outputChannelID'])).send('<@&{}>'.format(configFile['pingRoleID']), embed=embed)
            await reply.add_reaction('✅')
            await reply.add_reaction('❌')

            guild = client.get_guild(int(configFile['guildID']))
            role = guild.get_role(int(configFile['pingRoleID']))
            jumpUrl = reply.to_reference().jump_url

            for member in guild.members:
                if role in member.roles:
                    print('{}, {}'.format(member.name, member.roles))
                    await member.send('You have been invited to play a game!\nClick here ➡️ {}'.format(jumpUrl))

    except Exception as e:
        await message.channel.send(e)


def getCoverArt(query):
    url = 'https://www.google.com/search?q={0}&tbm=isch'.format(query)
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'html.parser')
    images = soup.findAll('img')

    return images[1].get('src')


client.run(token)
