from functions import *
from import_lib import *

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="ping", description="Shows the bots ping", with_app_command=True)
    async def ping(self, ctx: commands.Context):
        latency = round(self.bot.latency * 1000)  # Convert to milliseconds
        await ctx.send(f'Pong! Latency: {latency}ms')

async def setup(bot):
    await bot.add_cog(Ping(bot))
