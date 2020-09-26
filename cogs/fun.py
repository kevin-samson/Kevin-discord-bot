import re
from urllib import parse, request

import discord
from discord.ext import commands
import datetime
import random


class FunStuff(commands.Cog):
    def __int__(self, bot):
        self.bot = bot

    @commands.command(help="Gets persons pic using GRNO.")
    async def brs_pic(self, ctx, grno):
        try:
            av = discord.Embed(color=discord.Color.blue(), title="This is how " + str(grno) + " looks like",
                               timestamp=datetime.datetime.utcfromtimestamp(1600786335))
            av.set_author(name="Bright Riders School",
                          icon_url="https://pbs.twimg.com/profile_images/1044852220427218946"
                                   "/anG36qSn.jpg")
            av.set_image(
                url="http://ict-brs.ethdigitalcampus.com/container/school_data/BRS/photo/Student/" + str(grno) + ".jpg")
            await ctx.send(embed=av)
        except:
            await ctx.send("Nope,I can't find that grno")

    @commands.command(help="Simple calculator")
    async def cal(self, ctx, num):
        av = discord.Embed(color=discord.Color.blue(), title=f"The answer is : `{eval(num)}`")
        av.set_author(name="The calculator",
                      icon_url="https://is4-ssl.mzstatic.com/image/thumb/Purple123/v4/56/39/a0/5639a04b-3f9b-b7d0-87a2"
                               "-61b497b31ed4/pr_source.png/320x0w.png")
        await ctx.send(embed=av)

    @commands.command()
    async def f(self, ctx, *, text: commands.clean_content = None):
        """ Press F to pay respect """
        hearts = ['❤', '💛', '💚', '💙', '💜']
        reason = f"for **{text}** " if text else ""
        await ctx.send(f"**{ctx.author.name}** has paid their respect {reason}{random.choice(hearts)}")

    @commands.command(pass_context=True, help="Sends a direct message")
    async def dm(self, ctx, *, msg, member: discord.Member = None):
        if not member:
            av = discord.Embed(color=discord.Color.dark_gold(), title=f"{str(ctx.author)[:-5]} said : {msg}",
                               timestamp=datetime.datetime.utcfromtimestamp(1600786335))
            await ctx.author.send(embed=av)
            print(msg)
        else:
            av = discord.Embed(color=discord.Color.dark_gold(), title=f"{str(ctx.author)[:-5]} said : {msg}",
                               timestamp=datetime.datetime.utcfromtimestamp(1600786335))
            await member.send(embed=av)
        await ctx.send("Message has been sent")

    @commands.command(help="Dm everyone")
    @commands.guild_only()
    async def dma(self, ctx, *, msg):
        for user in ctx.guild.members:
            try:
                av = discord.Embed(color=discord.Color.dark_gold(), title=f"{str(ctx.author)[:-5]} said : {msg}",
                                   timestamp=datetime.datetime.utcfromtimestamp(1600786335))
                await user.send(embed=av)
            except:
                pass
        await ctx.send("Message has been sent")


def setup(bot):
    bot.add_cog(FunStuff(bot))
