from functions import *
from import_lib import *

class coins(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="coins", description="Shows the amount of coins", with_app_command=True)
    @commands.check(in_animal_shop)
    async def coins(self, ctx):
        try:
            # Get the user's balance from the database
            db = mysql.connector.connect(
                host="localhost", user="root", password="", database="reborn_legends"
            )
            cursor = db.cursor()
            cursor.execute(
                "SELECT coins FROM players WHERE discord_id = %s", (ctx.author.id,)
            )
            current_balance = cursor.fetchone()[0]

            # Send a message with the user's current balance
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description=f"Your current balance is {current_balance} :coin:.",
                color=0x00FF00,
            )
            await ctx.send(embed=embed)
        except Exception as e:
            # If an error occurs, send a message with the error details
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description=f"An error occurred while running the command:\n\n{str(e)}",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(coins(bot))
