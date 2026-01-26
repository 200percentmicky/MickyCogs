from .rngjesus import RNGJesus

async def setup(bot):
    await bot.add_cog(RNGJesus(bot))
