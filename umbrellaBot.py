import asyncio
from unicodedata import name
import discord
import dotenv
import requests

from bs4 import BeautifulSoup
from datetime import timedelta
from os import environ
from random import randint

debug = True
if 'UMBRELLABOT_DEV' not in environ:
    debug = False
else:
    print('Debug mode Enabled')

loop = asyncio.new_event_loop()
client = discord.Client(intents=discord.Intents.all(), loop=loop)


def main():
    if debug:
        open('.env', 'a+')
        dotenv.set_key('.env', 'UMBRELLABOT_DEV', 'True', quote_mode='never')
        dotenv.set_key(
            '.env', 'DEBUG_CHANNEL_ID', '926170088426573895', quote_mode='never'
        )
        dotenv.load_dotenv()

    print('Logging in...')
    try:
        client.run(environ['DISCORD_BOT_TOKEN'], reconnect=True)
    except Exception as e:
        print(e)

        token = input('Enter Discord Bot Token:\n')

        if not debug:
            environ['DISCORD_BOT_TOKEN'] = token
        else:
            dotenv.set_key('.env', 'DISCORD_BOT_TOKEN', token, quote_mode='never')


def getCoverArt(query):
    url = 'https://www.google.com/search?q={0}&tbm=isch'.format(query)
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'html.parser')
    images = soup.find_all('img')

    return images[1].get('src')


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
            await message.channel.send(
                'https://github.com/JoshuaVarga/Umbrellabot'
            )

        elif message.content.startswith('u!set'):
            if message.author.guild_permissions.administrator:
                match args[1]:
                    case 'GUILD_ID':
                        if not debug:
                            dotenv.set_key(
                                '.env', args[1], args[2], quote_mode='never'
                            )
                        else:
                            environ[args[1]] = args[2]
                    case 'OUTPUT_CHANNEL_ID':
                        if not debug:
                            dotenv.set_key(
                                '.env', args[1], args[2], quote_mode='never'
                            )
                        else:
                            environ[args[1]] = args[2]
                    case 'PING_ROLE_ID':
                        if not debug:
                            dotenv.set_key(
                                '.env', args[1], args[2], quote_mode='never'
                            )
                        else:
                            environ[args[1]] = args[2]

                await message.channel.send(
                    'Successfully updated {} to {}!'.format(args[1], args[2])
                )

            else:
                await message.channel.send('Insufficient privledges')

        elif message.content.startswith('u!game'):

            if int(args[2]) < 2 or int(args[2]) > float('inf'):
                raise Exception('Invalid range')

            def rnd(): return randint(0, 255)

            guild = client.get_guild(int(environ['GUILD_ID']))

            start_time = message.created_at + timedelta(minutes=int(args[3]))

            scheduledEvent = await guild.create_scheduled_event(
                name=args[1],
                start_time=start_time,
                location=guild.get_channel(int(environ['LOCATION_ID']))
            )

            embed = discord.Embed(
                type='rich',
                title='Needs {} people to play {}!'.format(args[2], args[1]),
                description='Click the RSVP button below for more details!',
                color=int('0x%02X%02X%02X' % (rnd(), rnd(), rnd()), 16),
                timestamp=start_time
            )

            embed.set_author(name=message.author.display_name)
            embed.set_footer(text="We're playing")
            embed.set_image(url=getCoverArt(args[1]))
            embed.set_thumbnail(url=str(message.author.avatar))

            if debug:
                channel = environ['DEBUG_CHANNEL_ID']
            else:
                channel = environ['OUTPUT_CHANNEL_ID']

            channel = int(channel)
            pingStr = ''

            if not debug:
                pingStr = '<@&{}>'.format(environ['PING_ROLE_ID'])

            btnViewEvent = discord.ui.Button(
                label='RSVP',
                url=scheduledEvent.url,
                style=discord.ButtonStyle.link
            )

            view = discord.ui.View()
            view.add_item(btnViewEvent)

            reply = await client.get_channel(channel).send(
                pingStr,
                embed=embed,
                view=view
            )

            if not debug:
                role = guild.get_role(int(environ['PING_ROLE_ID']))
                jumpUrl = reply.to_reference().jump_url

                for member in guild.members:
                    if role in member.roles and not debug:
                        try:
                            await member.send(
                                'You have been invited to play a game!\
                                \nClick here ➡️ {}'.format(jumpUrl)
                            )
                        except Exception as e:
                            continue

    except Exception as e:
        await message.channel.send(e)

if __name__ == '__main__':
    main()
