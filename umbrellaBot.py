from email.mime import image
import discord
import random
import requests

from bs4 import BeautifulSoup
from datetime import timedelta

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('u!help'):
        await client.get_channel(972571373748752404).send('ToDo')

    elif message.content.startswith('u!game'):
        args = message.content.split(' ')
        def rnd(): return random.randint(0, 255)

        embed = discord.Embed(
            type='rich',
            title='Needs {} people to play!'.format(args[2]),
            description='If you want to play react ✅ below!',
            color=int('0x%02X%02X%02X' % (rnd(), rnd(), rnd()), 16),
            timestamp=message.created_at + timedelta(minutes=int(args[3]))
        )

        embed.set_author(name=message.author.display_name)
        embed.set_footer(text="We're playing")
        embed.set_image(url=getCoverArt(args[1]))

        await client.get_channel(972571373748752404).send(embed=embed)


def getCoverArt(query):
    url = 'https://www.google.com/search?q={0}&tbm=isch'.format(query)
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'html.parser')
    images = soup.findAll('img')

    covers = []
    for image in images:
        covers.append(image.get('src'))

    return covers[1]

client.run('OTcyNTUzMzk5NTIwMzMzOTM1.GsjnXk.LvTo-6I0j3xPoKY7CX7NwxQdWk3U86_kWXG33Y')
