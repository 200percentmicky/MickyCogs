from .rpgdice import RPGDice

def setup(bot):
    bot.add_cog(RPGDice(bot))
