from .lizard import Lizard

async def setup(bot):
    await bot.add_cog(Lizard(bot))
