import aiohttp
import datetime
import discord

from redbot.core import commands, modlog, checks

async def timeout_user(bot, user_id: int, guild_id: int, reason: str, until):
    """
    Handshake to timeout users in minutes.
    """
    timeout = (datetime.datetime.utcnow() + datetime.timedelta(minutes=until)).isoformat()
    payload = {'communication_disabled_until': timeout}
    await bot.http.edit_member(guild_id, user_id, reason=reason, **payload)

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
    @checks.has_permissions()
    async def timeout(self, ctx: commands.Context, member: discord.Member, until: int, reason: str = None):
        """
        Timeout users on the server in minutes.

        `<member>` The member you want to put on timeout.
        `<until>` How long the member should be on timeout in minutes.
        `[reason]` The reason for the timeout.
        """
        async with ctx.typing():
            handshake = await timeout_user(self.bot, user_id=member.id, guild_id=ctx.guild.id, until=until, reason=reason)
            if handshake:
                await modlog.create_case(
                    ctx.bot, ctx.guild, ctx.message.created_at, action_type="timeout",
                    user=member, moderator=ctx.author, reason=reason
                )
                await ctx.send(f"Done. They'll be back in **{until}** minutes.")
            await ctx.send("Something went wrong")
