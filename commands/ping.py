from functions import *
from import_lib import *

class stop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def short(self, ctx):
        await ctx.send("Pong")

async def setup(bot):
    await bot.add_cog(stop(bot))
