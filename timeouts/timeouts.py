from datetime import datetime, timedelta
import discord

from redbot.core import commands, modlog, checks

async def timeout_payload(until: int = None):
    """
    Initial payload to provide to the API.
    """
    timeout = (datetime.utcnow() + timedelta(minutes=until)).isoformat() if until else None
    payload = {'communication_disabled_until': timeout}
    return payload

async def timeout_user(bot, user_id: int, guild_id: int, reason: str, until):
    """
    Timeout users in minutes.
    """
    member = await bot.http.get_member(guild_id, user_id)
    if member['communication_disabled_until'] is None:
        return await bot.http.edit_member(guild_id, user_id, reason=reason, **timeout_payload(until))
    else:
        raise discord.HTTPException("Communications for member is already restricted.")

async def untimeout_user(bot, user_id: int, guild_id: int, reason: str):
    """
    Removes the timeout from the user.
    """
    member = await bot.http.get_member(guild_id, user_id)
    if member['communication_disabled_until'] is not None:
        return await bot.http.edit_member(guild_id, user_id, reason=reason, **timeout_payload(None))
    else:
        raise discord.HTTPException("Communications for member is not restricted.")

class Timeouts(commands.Cog):
    """
    Timeouts for Red V3

    For this cog to work, you need to have a mod role set, or use the permissions cog to adjust access accordingly.
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
                "case_str": "Timeout"
            },
            {
                "name": "remove_timeout",
                "default_setting": True,
                "image": "💥",
                "case_str": "Timeout"
            }
        ]

        try:
            await modlog.register_casetype(timeout_types)
        except RuntimeError:
            pass

    @commands.command()
    @checks.mod() # Recommended. The library doesn't have the "Moderate Members" permission stored, so bits will be used.
    async def timeout(self, ctx: commands.Context, member: discord.Member, until: int, *, reason: str = None):
        """
        Puts a member on timeout with the time specified in minutes.

        `<member>` The member you want to put on timeout.
        `<until>` How long the member should be on timeout in minutes.
        `[reason]` The reason for the timeout.

        For this command to work, you need to have a mod role set, or use the permissions cog to adjust access accordingly.
        """

        if ctx.author.id == ctx.user.id:
            return await ctx.send(":warning: You can't place yourself on timeout.")

        try:
            async with ctx.typing():
                await timeout_user(self.bot, user_id=member.id, guild_id=ctx.guild.id, until=until, reason=reason)
                await modlog.create_case(
                    ctx.bot, ctx.guild, ctx.message.created_at, action_type="timeout",
                    user=member, moderator=ctx.author, reason=reason,
                    until=datetime.utcnow() + timedelta(minutes=until)
                )
                await ctx.send(f":white_check_mark: Done. Time away will do good.")
        except discord.Forbidden:
            return await ctx.send(":warning: I'm not allow to do that.")
        except discord.HTTPException:
            return await ctx.send(":warning: That user is already on timeout.")

    @commands.command()
    @checks.mod() # Recommended. The library doesn't have the "Moderate Members" permission stored, so bits will be used.
    async def untimeout(self, ctx: commands.Context, member: discord.Member, *, reason: str = None):
        """
        Removes a members timeout, if one is in place.

        `<member>` The member you want to remove the timeout from.
        `[reason]` The reason for removing their timeout.

        For this command to work, you need to have a mod role set, or use the permissions cog to adjust access accordingly.
        """

        if ctx.author.id == ctx.user.id:
            return await ctx.send(":warning: You can't place yourself on timeout.")

        try:
            async with ctx.typing():
                await timeout_user(self.bot, user_id=member.id, guild_id=ctx.guild.id, until=None, reason=reason)
                await modlog.create_case(
                    ctx.bot, ctx.guild, ctx.message.created_at, action_type="remove_timeout",
                    user=member, moderator=ctx.author, reason=reason
                )
                await ctx.send(f":white_check_mark: Done. Time away will do good.")
        except discord.Forbidden:
            return await ctx.send(":warning: I'm not allow to do that.")
        except discord.HTTPException:
            return await ctx.send(":warning: That user isn't on timeout.")
