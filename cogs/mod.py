import discord
import re
import asyncio
from io import BytesIO

from discord.ext import commands
from utils import permissions, default


class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.guild_only()
    @commands.max_concurrency(1, per=commands.BucketType.guild)
    @permissions.has_permissions(manage_messages=True)
    async def prune(self, ctx):
        """ Removes messages from the current server. """
        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))

    async def do_removal(self, ctx, limit, predicate, *, before=None, after=None, message=True):
        if limit > 2000:
            return await ctx.send(f'Too many messages to search given ({limit}/2000)')

        if before is None:
            before = ctx.message
        else:
            before = discord.Object(id=before)

        if after is not None:
            after = discord.Object(id=after)

        try:
            deleted = await ctx.channel.purge(limit=limit, before=before, after=after, check=predicate)
        except discord.Forbidden:
            return await ctx.send('I do not have permissions to delete messages.')
        except discord.HTTPException as e:
            return await ctx.send(f'Error: {e} (try a smaller search?)')

        deleted = len(deleted)
        if message is True:
            await ctx.send(f'🚮 Successfully removed {deleted} message{"" if deleted == 1 else "s"}.')

    @prune.command()
    async def embeds(self, ctx, search=100):
        """Removes messages that have embeds in them."""
        await self.do_removal(ctx, search, lambda e: len(e.embeds))

    @prune.command()
    async def files(self, ctx, search=100):
        """Removes messages that have attachments in them."""
        await self.do_removal(ctx, search, lambda e: len(e.attachments))

    @prune.command()
    async def mentions(self, ctx, search=100):
        """Removes messages that have mentions in them."""
        await self.do_removal(ctx, search, lambda e: len(e.mentions) or len(e.role_mentions))

    @prune.command()
    async def images(self, ctx, search=100):
        """Removes messages that have embeds or attachments."""
        await self.do_removal(ctx, search, lambda e: len(e.embeds) or len(e.attachments))

    @prune.command(name='all')
    async def _remove_all(self, ctx, search=100):
        """Removes all messages."""
        await self.do_removal(ctx, search, lambda e: True)

    @prune.command()
    async def user(self, ctx, member: discord.Member, search=100):
        """Removes all messages by the member."""
        await self.do_removal(ctx, search, lambda e: e.author == member)

    @prune.command()
    async def contains(self, ctx, *, substr: str):
        """Removes all messages containing a substring.
        The substring must be at least 3 characters long.
        """
        if len(substr) < 3:
            await ctx.send('The substring length must be at least 3 characters.')
        else:
            await self.do_removal(ctx, 100, lambda e: substr in e.content)

    @prune.command(name='bots')
    async def _bots(self, ctx, search=100, prefix=None):
        """Removes a bot user's messages and messages with their optional prefix."""

        getprefix = prefix if prefix else "kek "

        def predicate(m):
            return (m.webhook_id is None and m.author.bot) or m.content.startswith(tuple(getprefix))

        await self.do_removal(ctx, search, predicate)

    @prune.command(name='users')
    async def _users(self, ctx, prefix=None, search=100):
        """Removes only user messages. """

        def predicate(m):
            return m.author.bot is False

        await self.do_removal(ctx, search, predicate)

    @prune.command(name='emojis')
    async def _emojis(self, ctx, search=100):
        """Removes all messages containing custom emoji."""
        custom_emoji = re.compile(r'<a?:(.*?):(\d{17,21})>|[\u263a-\U0001f645]')

        def predicate(m):
            return custom_emoji.search(m.content)

        await self.do_removal(ctx, search, predicate)

    @prune.command(name='reactions')
    async def _reactions(self, ctx, search=100):
        """Removes all reactions from messages that have them."""

        if search > 2000:
            return await ctx.send(f'Too many messages to search for ({search}/2000)')

        total_reactions = 0
        async for message in ctx.history(limit=search, before=ctx.message):
            if len(message.reactions):
                total_reactions += sum(r.count for r in message.reactions)
                await message.clear_reactions()

        await ctx.send(f'Successfully removed {total_reactions} reactions.')

    @commands.command()
    @commands.guild_only()
    async def kick(self, ctx, member: discord.Member, *, reason: str = None):
        """ Kicks a user from the current server. """
        if await permissions.check_priv(ctx, member):
            return

        try:
            await member.kick(reason=default.responsible(ctx.author, reason))
            await ctx.send(default.actionmessage("kicked"))
        except Exception as e:
            await ctx.send(e)

def setup(bot):
    bot.add_cog(Moderator(bot))
