import requests
from redbot.core import commands

class ChuckNorris(commands.Cog):
    """
    Chuck Norris Facts

    [Chuck Norris can unscrable eggs.](https://api.chucknorris.io/)
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="chucknorris")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def chuck_norris(self, ctx: commands.Context):
        """
        Get a random Chuck Norris fact.
        """
        await ctx.trigger_typing()
        
        r = requests.get("https://api.chucknorris.io/jokes/random")
        data = r.json()["value"]

        await ctx.send(data)

def setup(bot):
    bot.add_cog(ChuckNorris(bot))