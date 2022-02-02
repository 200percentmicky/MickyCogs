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
    return await bot.http.edit_member(guild_id, user_id, reason=reason, **timeout_payload(until))

async def untimeout_user(bot, user_id: int, guild_id: int, reason: str):
    """
    Removes the timeout from the user.
    """
    return await bot.http.edit_member(guild_id, user_id, reason=reason, **timeout_payload(None))

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
        timeout_type = {
            "name": "timeout",
            "default_setting": True,
            "image": "\N{TIMER CLOCK}",
            "case_str": "Timeout"
        }

        try:
            await modlog.register_casetype(**timeout_type)
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
        """
        if not ctx.guild.me.guild_permissions.value(1 << 40):
            return await ctx.send(":warning: I don't have the **Moderate Members** permission to do that.")

        if not ctx.author.guild_permissions.value(1 << 40):
            return await ctx.send(":warning: You need the **Moderate Members** permission to do that.")

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
