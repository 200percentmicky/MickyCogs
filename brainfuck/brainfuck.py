"""
Brainfuck cog.
"""

"""
MIT License

Copyright (c) 2021-present Micky | @200percentmicky

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import brainfuck
from redbot.core import commands

# Tried writing an interpreter lol, gave up halfway.

class Brainfuck(commands.Cog):
    """
    Brainfuck

    A programming language that's designed to make your brain hurt.
    Learn how to use brainfuck [here](https://esolangs.org/wiki/Brainfuck)
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name=brainfuck)
    async def brainfuck(self, ctx: commands.Context, *, syntax: str):
        """
        Interpret a string in brainfuck.
        """
        bf = syntax

        try:
            await ctx.send(brainfuck.evaluate(bf))
        except Exception as e:
            await ctx.send(content=e)
