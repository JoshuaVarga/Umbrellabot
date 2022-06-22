# ----------------------------------IMPORTS-------------------------------------
import discord
import dotenv
import requests

from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
from os import environ
from random import randint

# ----------------------------------GLOBALS-------------------------------------
debug = True
bot = discord.Bot(command_prefix='u!', intents=discord.Intents.all())

# ---------------------------------FUNCTIONS------------------------------------
def main():
    global debug

    if 'UMBRELLABOT_DEV' not in environ:
        debug = False
    else:
        print('Debug mode Enabled')
        open('.env', 'a+')
        dotenv.load_dotenv()

    bot.activity = discord.Activity(name='/game', type=3)

    print('Logging in...')
    try:
        bot.run(environ['DISCORD_BOT_TOKEN'], reconnect=True)
    except Exception as e:
        print(e)

def getCoverArt(query):
    '''
    Returns a URL of an image relevant to the search query.

        Parameters:
            query (str): string to find an image for

        Returns:
            URL of image relevant to the query
    '''

    url = 'https://www.google.com/search?q={0}&tbm=isch'.format(query)
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'html.parser')
    images = soup.find_all('img')

    return images[1].get('src')

# ----------------------------------EVENTS--------------------------------------
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

# ----------------------------------COMMANDS------------------------------------
@bot.command(description='Schedule a time to play a game')
async def game(
    ctx: discord.ApplicationContext,
    name: discord.Option(
        str,
        'Enter the name of the game you want to play',
    ),
    player_count: discord.Option(
        int,
        'Enter the amount of players needed to play',
        min_value=2
    ),
    time: discord.Option(
        int,
        'Enter the amount of minutes from now until when you want to play',
        min_value=1
    )
):
    def rnd(): return randint(0, 255)   # Generates random colour value

    guild = bot.get_guild(int(environ['GUILD_ID']))

    # Create Discord Scheduled Event
    start_time = datetime.now(timezone.utc) + timedelta(minutes=time)
    scheduledEvent = await guild.create_scheduled_event(
        name=name,
        start_time=start_time,
        location=guild.get_channel(int(environ['LOCATION_ID']))
    )

    # Create Discord Message
    pingStr = ''

    if not debug:
        pingStr = '<@&{}>'.format(environ['PING_ROLE_ID'])

    # Create Discord Embed
    embed = discord.Embed(
        type='rich',
        title='Needs {} people to play {}!'.format(player_count, name),
        description='Click the RSVP button below for more details!',
        color=int('0x%02X%02X%02X' % (rnd(), rnd(), rnd()), 16),
        timestamp=start_time
    )

    embed.set_author(name=ctx.interaction.user.display_name)
    embed.set_footer(text="We're playing")
    embed.set_image(url=getCoverArt(name))
    embed.set_thumbnail(url=str(ctx.interaction.user.avatar))

    # Create Discord Button and add it to a View
    btnViewEvent = discord.ui.Button(
        label='RSVP',
        url=scheduledEvent.url,
        style=discord.ButtonStyle.link
    )

    view = discord.ui.View()
    view.add_item(btnViewEvent)

    # Get output channel
    channel = environ['OUTPUT_CHANNEL_ID']

    if debug:
        channel = environ['DEBUG_CHANNEL_ID']

    # Combine everything together and send as a Discord message
    reply = await bot.get_channel(int(channel)).send(
        pingStr,
        embed=embed,
        view=view
    )

    # PM role members that they've been invited to play a game
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

    await ctx.respond('Game successfully scheduled!')


@bot.command(description='Set a key value to a Discord ID')
@discord.default_permissions(administrator=True)
async def set(
    ctx: discord.ApplicationContext,
    key: discord.Option(
        str,
        'Choose the key whose value you wish to change',
        choices=['GUILD_ID', 'OUTPUT_CHANNEL_ID', 'PING_ROLE_ID']
    ),
    value: discord.Option(str, 'Enter the ID value')
):
    if debug:
        dotenv.set_key(
            '.env', key, value, quote_mode='never'
        )
    else:
        environ[key] = value

    await ctx.respond('Successfully set {} to {}!'.format(key, value))

# -----------------------------------MAIN---------------------------------------
if __name__ == '__main__':
    main()