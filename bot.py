import discord

from cogs.Scheduling import Scheduling
from dotenv import load_dotenv
from os import environ

load_dotenv()

initial_cogs = [
    Scheduling
]

class Umbrellabot(discord.Bot):
    debug: bool
    output_channel_id: int
    location_id: int


    def __init__(self) -> None:
        super().__init__(intents=discord.Intents.all())
        self.activity = discord.Activity(
            name='/game',
            type=discord.ActivityType.playing
        )
        self.debug = 'UMBRELLABOT_DEV' in environ
        self.output_channel_id = int(environ['OUTPUT_CHANNEL_ID'])
        self.location_id = int(environ['LOCATION_ID'])

    async def on_ready(self) -> None:
        print(f'Logged in as: {self.user}')
        if self.debug: print('Debug mode enabled')

    def load_cogs(self) -> None:
        for cog in initial_cogs:
            self.add_cog(cog(self))

def run() -> None:
    bot = Umbrellabot()
    bot.load_cogs()
    bot.run(environ['DISCORD_BOT_TOKEN'], reconnect=True)

if __name__ == '__main__':
    run()