from datetime import datetime, timedelta
import discord

from redbot.core import commands, modlog, checks

class InTimeout(Exception):
    """
    Exception for when a member is on timeout.
    """
    pass

class NotInTimeout(Exception):
    """
    Exception for when a member is not in timeout.
    """
    pass

class TimeExceeded(Exception):
    """
    Raised when the time provided exceeds the limits of 28 days. (40320 minutes)
    """
    pass

def timeout_payload(until: int = None):
    """
    Initial payload to provide to the API.
    """
    timeout = (datetime.utcnow() + until).isoformat() if until else None
    payload = {'communication_disabled_until': timeout}
    return payload

async def timeout_user(bot, user_id: int, guild_id: int, reason: str, until):
    """
    Timeout users in minutes.
    """
    if until > timedelta(days=28):
        raise TimeExceeded()
    member = await bot.http.get_member(guild_id, user_id)
    if not member['communication_disabled_until']:
        return await bot.http.edit_member(guild_id, user_id, reason=reason, **timeout_payload(until - timedelta(seconds=1)))
    else:
        raise InTimeout()

async def untimeout_user(bot, user_id: int, guild_id: int, reason: str):
    """
    Removes the timeout from the user.
    """
    member = await bot.http.get_member(guild_id, user_id)
    if member['communication_disabled_until']:
        return await bot.http.edit_member(guild_id, user_id, reason=reason, **timeout_payload(None))
    else:
        raise NotInTimeout()

class Timeouts(commands.Cog):
    """
    Timeouts for Red V3
    """

    def __init__(self, bot):
        self.bot = bot

    async def initialize(self):
        await self.register_casetypes()

    @staticmethod
    async def register_casetypes():
        timeout_types = [
            {
                "name": "timeout",
                "default_setting": True,
                "image": "\N{TIMER CLOCK}",
                "case_str": "Timed Mute"
            },
            {
                "name": "remove_timeout",
                "default_setting": True,
                "image": "💥",
                "case_str": "Remove Timed Mute"
            }
        ]

        try:
            await modlog.register_casetypes(timeout_types)
        except RuntimeError:
            pass

    @commands.command()
    @checks.mod() # Recommended. The library doesn't have the "Moderate Members" permission stored, so bits will be used.
    async def timeout(
        self,
        ctx: commands.Context,
        member: discord.Member,
        until: commands.TimedeltaConverter, 
        *,
        reason: str = None
    ):
        """
        Puts a member on timeout with the time specified in minutes.

        `<member>` The member you want to put on timeout.
        `<until>` How long the member should be on timeout in minutes.
        `[reason]` The reason for the timeout.
        """

        if ctx.author.id == member.id:
            return await ctx.send("You can't place yourself on timeout.")

        try:
            async with ctx.typing():
                await timeout_user(self.bot, user_id=member.id, guild_id=ctx.guild.id, until=until, reason=reason)
                await modlog.create_case(
                    ctx.bot, ctx.guild, ctx.message.created_at, action_type="timeout",
                    user=member, moderator=ctx.author, reason=reason,
                    until=datetime.utcnow() + until - timedelta(seconds=1)
                )
                await ctx.send("Done. Time away will do them good.")
        except discord.Forbidden:
            await ctx.send("I'm not allow to do that for some reason.")
        except TimeExceeded:
            await ctx.send("Invalid time given. Max time is 28 days.")
        except InTimeout:
            await ctx.send("That member is already on timeout.")


    @commands.command()
    @checks.mod() # Recommended. The library doesn't have the "Moderate Members" permission stored, so bits will be used.
    async def untimeout(self, ctx: commands.Context, member: discord.Member, *, reason: str = None):
        """
        Removes a members timeout, if one is in place.

        `<member>` The member you want to remove the timeout from.
        `[reason]` The reason for removing their timeout.
        """

        if ctx.author.id == member.id:
            return await ctx.send("You can't place yourself on timeout.")

        try:
            async with ctx.typing():
                await untimeout_user(self.bot, user_id=member.id, guild_id=ctx.guild.id, reason=reason)
                await modlog.create_case(
                    ctx.bot, ctx.guild, ctx.message.created_at, action_type="remove_timeout",
                    user=member, moderator=ctx.author, reason=reason
                )
                await ctx.send(f"Done. Hope they learned their lesson.")
        except discord.Forbidden:
            await ctx.send("I'm not allow to do that.")
        except NotInTimeout:
            await ctx.send("That member is not in timeout.")
