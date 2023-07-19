from .chronosdelta import ChronosDelta

async def setup(bot):
    await bot.add_cog(ChronosDelta(bot))
