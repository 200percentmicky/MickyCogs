from .chucknorris import ChuckNorris

async def setup(bot):
    await bot.add_cog(ChuckNorris(bot))
