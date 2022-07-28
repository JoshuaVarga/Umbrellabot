import discord

from datetime import datetime, timedelta, timezone
from utils.cover_art import cover_art
from utils.find_thread import find_thread
from utils.random_rgb import random_rgb

class Scheduling(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot

    @discord.command(description='Schedule a time to play a game')
    async def game(
        self,
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
        guild = ctx.interaction.guild

        # Create Discord Scheduled Event
        start_time = datetime.now(timezone.utc) + timedelta(minutes=time)
        scheduledEvent = await guild.create_scheduled_event(
            name=name,
            start_time=start_time,
            location=self.bot.location_id
        )

        # Create Discord Message
        pingStr = ''

        if not self.bot.debug:
            pingStr = f'{guild.default_role}'

        # Create Discord Embed
        embed = discord.Embed(
            type='rich',
            title='Needs {} people to play {}!'.format(player_count, name),
            description='Click the RSVP button below for more details!',
            color=int('0x%02X%02X%02X' % random_rgb(), 16),
            timestamp=start_time
        )

        embed.set_author(name=ctx.interaction.user.display_name)
        embed.set_footer(text="We're playing")
        embed.set_image(url=cover_art(name))
        embed.set_thumbnail(url=str(ctx.interaction.user.avatar))

        # Create Discord Button and add it to a View
        btnViewEvent = discord.ui.Button(
            label='RSVP',
            url=scheduledEvent.url,
            style=discord.ButtonStyle.link
        )

        btnCreateThread = discord.ui.Button(
            custom_id='btnCreateThread',
            style=discord.ButtonStyle.secondary,
            label='Create Thread',
            emoji='#️⃣'
        )

        id = self.bot.output_channel_id

        # Get output channel
        if self.bot.debug:
            id = ctx.interaction.channel_id

        channel = self.bot.get_channel(int(id))

        view = discord.ui.View(timeout=None)
        view.add_item(btnViewEvent)
        view.add_item(btnCreateThread)

        thread = await find_thread(name, channel)

        if thread != None:
            if thread.archived:
                await thread.unarchive()
            channel = thread
            view.remove_item(btnCreateThread)

        print(channel.name)

        # Combine everything together and send as a Discord message
        reply = await channel.send(
            pingStr,
            embed=embed,
            view=view
        )

        async def btnCallback(interaction):
            btnCreateThread.disabled = True
            await reply.edit(view=view)
            msg = await channel.send('{} Thread'.format(name))
            await msg.create_thread(name=name)

            await interaction.response.defer()

        btnCreateThread.callback = btnCallback

        # PM role members that they've been invited to play a game
        # if not debug:
        #     role = guild.get_role(int(environ['PING_ROLE_ID']))
        #     jumpUrl = reply.to_reference().jump_url

        #     for member in guild.members:
        #         if role in member.roles and not debug:
        #             try:
        #                 await member.send(
        #                     'You have been invited to play a game!\
        #                     \nClick here ➡️ {}'.format(jumpUrl)
        #                 )
        #             except Exception as e:
        #                 continue

        await ctx.interaction.response.send_message(
            content='Event successfully scheduled!',
            ephemeral=True
        )