import aiohttp
import datetime
import discord

from redbot.core import commands, modlog, checks

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

    # https://stackoverflow.com/questions/70459488/discord-py-timeout-server-members
    # A handshake must be made to Discord since Timeouts aren't implemented in discord.py

    async def timeout_user(bot, user_id: int, guild_id: int, until):
        """
        Handshake to timeout users in minutes.
        """
        headers = {"Authorization": f"Bot {bot.http.token}"}
        url = f"https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}"
        timeout = (datetime.datetime.utcnow() + datetime.timedelta(minutes=until)).isoformat()
        params = {'communication_disabled_until': timeout}
        async with aiohttp.ClientSession() as session:
            async with session.patch(url, params=params, headers=headers) as response:
                if response.status in range(200, 299):
                    return True
                return False


    @commands.command()
    @checks.has_permissions()
    async def timeout(self, ctx: commands.Context, member: discord.Member, until: int, reason: str = None):
        """
        Timeout users on the server in minutes.

        `<member>` The member you want to put on timeout.
        `<until>` How long the member should be on timeout in minutes.
        `[reason]` The reason for the timeout.
        """
        handshake = await timeout_user(self.bot, user_id=member.id, guild_id=ctx.guild.id, until=until)
        if handshake:
            await modlog.create_case(
                ctx.bot, ctx.guild, ctx.message.created_at, action_type="timeout",
                user=member, moderator=ctx.author, reason=reason
            )
            await ctx.send(f"Done. They'll be back in **{until}** minutes.")
        await ctx.send("Something went wrong")
