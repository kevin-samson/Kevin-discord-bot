import time
import discord
import psutil
import os

from datetime import datetime
from discord.ext import commands
from utils import default

owners = [663816878921351178]


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process(os.getpid())

    @commands.command(help='shows ping')
    async def ping(self, ctx):
        await ctx.send(f'this ping doesn\'t mean anything really: `{round(self.bot.latency * 1000)}ms` ')

    @commands.command(aliases=['info', 'stats', 'status'])
    async def about(self, ctx):
        """ About the bot """
        ramUsage = self.process.memory_full_info().rss / 1024 ** 2
        avgmembers = round(len(self.bot.users) / len(self.bot.guilds))

        embedColour = discord.Color.blue()
        if hasattr(ctx, 'guild') and ctx.guild is not None:
            embedColour = discord.Color.blue()  # ctx.me.top_role.colour

        embed = discord.Embed(colour=embedColour)
        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        embed.add_field(
            name=f"Developer{'' if len(owners) == 1 else 's'}",
            value=', '.join([str(self.bot.get_user(x)) for x in owners]),
            inline=True)
        embed.add_field(name="Last boot", value=default.timeago(datetime.now() - self.bot.uptime), inline=True)
        embed.add_field(name="Library", value="discord.py", inline=True)
        embed.add_field(name="Servers", value=f"{len(ctx.bot.guilds)} ( avg: {avgmembers} users/server )", inline=True)
        embed.add_field(name="Commands loaded", value=str(len([x.name for x in self.bot.commands])), inline=True)
        embed.add_field(name="RAM", value=f"{ramUsage:.2f} MB", inline=True)

        await ctx.send(content=f"ℹ About **{ctx.bot.user}** | **{1.0}**", embed=embed)
       

    @commands.command(aliases=['joinme', 'join', 'botinvite'])
    async def invite(self, ctx):
        """ Invite me to your server """
        await ctx.send(
            f"**{ctx.author.name}**, use this URL to invite me\n<{discord.utils.oauth_url(self.bot.user.id)}>")


def setup(bot):
    bot.add_cog(Information(bot))
