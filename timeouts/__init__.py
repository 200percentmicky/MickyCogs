from .timeouts import Timeouts

async def setup(bot):
    await Timeouts().initialize(bot)
    bot.add_cog(Timeouts(bot))
