import discord
import d20

from redbot.core import commands, checks

class RPGDice(commands.Cog):
    """
    RPG Dice
    Built using Avrae's D20 library.
    """
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("roll")

    @commands.command()
    @checks.bot_has_permissions(embed_links=True)
    async def roll(self, ctx, *, dice_expression):
        """
        Rolls a dice expression.

        **[Full Documentation](https://raw.githubusercontent.com/avrae/d20/master/README.md)**

        **Examples**
        4d6kh3 (4, 4, **6**, ~~3~~) = `14`
        2d6ro<3 (**~~1~~**, 3, **6**) = `9`
        8d6mi2 (1 -> 2, **6**, 4, 2, **6**, 2, 5, **6**) = `33`
        (1d4 (2) + 1, ~~3~~, ~~2d6kl1 (2, 5)~~)kh1 = `3`

        **Operators**
        `k` keep | `p` drop | `rr` reroll | `ro` reroll once | `ra` reroll and add | 
        `e` explode on | `mi` minimum | `ma` maximum

        **Selectors**
        `X` literal | `hX` highest X | `lX` lowest X | `>X` greater than X |
        `<X` less than X |

        **Unary Operations**
        `+X` positive | `-X` negative

        **Binary Operations**
        `X * Y` multiplication | `X / Y` division | `X // Y` int division 
        `X % Y` modulo | `X + Y` addition | `X - Y` subtraction | `X == Y` equality
        `X >= Y` greater/equal | `X <= Y` less/equal | `X > Y` greater than
        `X < Y` less than | `X != Y` inequality

        """
        try:
            r = d20.roll(dice_expression)            
            
            result = r.result
            total = r.total

            msg = f"{ctx.author.mention}  |  :game_die: **{total}**"
            
            if len(result) < 2000:
                embed = discord.Embed(
                    color=0xFFFFFF,
                    description=result
                )
                await ctx.send(content=msg, embed=embed)
            else:
                await ctx.send(msg)
        except d20.TooManyRolls:
            await ctx.send(f":warning: {ctx.author.mention}, that's too much dice! Please roll a lower number.")
            return
        except d20.RollError:
            await ctx.send(f":x: `{dice_expression}` is not a valid dice expression.")
            return

def setup(bot):
    bot.add_cog(RPGDice(bot))