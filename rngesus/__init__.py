from .rngesus import RNGesus

async def setup(bot):
    await bot.add_cog(RNGesus(bot))
