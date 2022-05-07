import discord

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run('OTcyNTUzMzk5NTIwMzMzOTM1.GsjnXk.LvTo-6I0j3xPoKY7CX7NwxQdWk3U86_kWXG33Y')