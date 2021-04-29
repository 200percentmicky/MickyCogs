import pytz
import discord
from redbot.core import commands, Config, checks
from datetime import datetime

class ChronosDelta(commands.Cog):
    """
    Chronos Delta

    A fully functioning clock for your Discord server. =)

    A rewrite of one of my bots that basically adds an internal clock to your server.
    """

    guild_defaults = {
        "timezone": None
    }

    user_defaults = {
        "timezone": None
    }

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 805470788, force_registration=True)
        self.config.register_guild(**self.guild_defaults)
        self.config.register_user(**self.user_defaults)

    @commands.command(name="time")
    @commands.guild_only()
    async def time(self, ctx: commands.Context, *, user: discord.Member = None):
        """
        Shows the current time on the server.

        If a user is provided, shows you the time for that specific user only 
        if that user has a time zone set.
        
        If no time zone is specified, defaults to Universal Time Coordinate (UTC). 
        To specify a time zone for your server, use `[p]settimezone server`.
        """
        timezone_setting = await self.config.guild(ctx.guild).timezone()

        if user:
            if user == 'me':
                user = ctx.author.id
            timezone_setting = await self.config.user(user).timezone()
            if timezone_setting is None:
                return await ctx.send("⚠ That user doesn't have a timezone.")

        time_zone = pytz.timezone(timezone_setting if timezone_setting is not None else "UTC")
        current = datetime.now(tz=time_zone)
        date = current.strftime("%A, %B %d, %Y")
        time = current.strftime("%I:%M %p")

        emoji_clock = {
            '00': '🕛',
            '01': '🕐',
            '02': '🕑',
            '03': '🕒',
            '04': '🕓',
            '05': '🕔',
            '06': '🕕',
            '07': '🕖',
            '08': '🕗',
            '09': '🕘',
            '10': '🕙',
            '11': '🕚',
            '12': '🕛',
            '13': '🕐',
            '14': '🕑',
            '15': '🕒',
            '16': '🕓',
            '17': '🕔',
            '18': '🕕',
            '19': '🕖',
            '20': '🕗',
            '21': '🕘',
            '22': '🕙',
            '23': '🕚'
        }
        hour = current.strftime("%I")

        try:
            embed = discord.Embed(
                color=user.color if user is not None else ctx.me.color,
                description="📅 {date}\n{emoji} {time}".format(
                    date=date,
                    emoji=emoji_clock[hour],
                    time=time.lstrip("0")
                )
            )
            
            embed.set_author(
                name=user if user is not None else ctx.guild.name,
                icon_url=user.avatar_url if user is not None else ctx.guild.icon_url
            )

            embed.set_footer(
                text="Time Zone: {tz}".format(tz=time_zone)
            )

            try:
                await ctx.message.add_reaction(emoji_clock[hour])
            except discord.Forbidden:
                pass
            await ctx.reply(embed=embed, delete_after=10, mention_author=True)
        except discord.Forbidden:
            try:
                await ctx.message.add_reaction(emoji_clock[hour])
            except discord.Forbidden:
                pass
            await ctx.reply("📅 {date}\n{emoji} {time}\n:globe_with_meridians: {tz}".format(
                date=date,
                emoji=emoji_clock[hour],
                time=time.lstrip("0"),
                tz=time_zone
            ), delete_after=10)

    @commands.group()
    @commands.guild_only()
    async def settimezone(self, ctx: commands.Context):
        """
        Time Zone Management

        You can set a time zone for the server, or for yourself! Must be in a 
        TZ database format.
        
        Visit https://en.wikipedia.org/wiki/List_of_tz_database_time_zones for 
        a list of compatible time zones.
        """
    
    @settimezone.command(name="server")
    @checks.has_permissions(manage_guild=True)
    async def server(self, ctx: commands.Context, *, timezone = None):
        """
        Sets the server's time zone.
        """

        if timezone in pytz.all_timezones:
            await self.config.guild(ctx.guild).timezone.set(timezone)
            await ctx.reply("✅ The time zone for **{guild}** is now `{tz}`".format(
                guild=ctx.guild.name,
                tz=timezone
            ))
        else:
            if timezone is None:
                await self.config.guild(ctx.guild).clear_raw()
                return await ctx.reply("✅ The time zone for **{guild}** is now `UTC`".format( # Hard coded. lol
                    guild=ctx.guild.name
                ))
            await ctx.reply("❌ `{tz}` is not valid time zone. Please visit **{url}** for a list of compatible time zones.".format(
                tz=timezone,
                url="https://en.wikipedia.org/wiki/List_of_tz_database_time_zones"
            ))

    @settimezone.command(name="user")
    async def user(self, ctx: commands.Context, *, timezone = None):
        """
        Sets a time zone for yourself.

        This is applied globally. People will be able to look up your current time as 
        long as you share a mutual server of that server the command is used in.
        """

        if timezone in pytz.all_timezones:
            await self.config.user(ctx.author).timezone.set(timezone)
            return await ctx.reply("✅ Your time zone is now `{tz}`".format(tz=timezone))
        else:
            if timezone is None:
                await self.config.user(ctx.author).clear_raw()
                return await ctx.send("ℹ Your time zone has been removed successfully.")
            await ctx.reply("❌ `{tz}` is not valid time zone. Please visit **{url}** for a list of compatible time zones.".format(
                tz=timezone,
                url="https://en.wikipedia.org/wiki/List_of_tz_database_time_zones"
            ))
