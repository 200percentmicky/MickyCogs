from .rngjesus import RPGDice

async def setup(bot):
    await bot.add_cog(RPGDice(bot))
