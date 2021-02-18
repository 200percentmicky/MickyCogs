from .chucknorris import ChuckNorris

def setup(bot):
    bot.add_cog(ChuckNorris(bot))
