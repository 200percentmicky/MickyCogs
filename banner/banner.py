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

import discord
from redbot.core import commands

class Banner(commands.Cog):
    """
    Give your bot a banner!

    :warning: **Experimental:** Uses an undocumented endpoint and may change at any time.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(name="banner")
    async def banner(self, ctx: commands.Context):
        """
        Sets [botname]'s banner image. An image must be attached. Supported
        formats are PNG, JPEG, and GIF.
        """

        image = {
            banner: discord.utils._bytes_to_base64_data(await ctx.message.attachments[0].read())
        }

        try:
            await bot.http.edit_profile(image)
        except discord.HTTPException as e:
            await ctx.send(f'An error occured in the request. {e}')
        except Exception as e:
            await ctx.send(f"Failed to set the banner image. {e}")