from functions import *
from import_lib import *
from datetime import datetime, timedelta

class work(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(in_animal_shop)
    async def work(self, ctx):
        player_data = get_player_data(ctx.author.id)

        # Check if the player has linked their Steam ID
        if player_data is None or player_data["steam_id"] is None:
            embed = discord.Embed(
                title="Reborn Legends 🤖",
                description=f"{ctx.author.mention}, you need to link your Steam ID first using the !link command.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        # Get the last_work_time from the player's data
        last_work_time = player_data.get("last_work_time") or datetime.min
        current_time = datetime.now()

        # Calculate the time difference
        time_difference = current_time - last_work_time

        if time_difference >= timedelta(hours=1):
            # Generate a random amount of coins between 500-2000
            coins_earned = random.randint(350, 1250)

            # Update the user's balance in the database
            db = mysql.connector.connect(
                host="localhost", user="root", password="", database="reborn_legends"
            )
            cursor = db.cursor()
            cursor.execute("SELECT coins FROM players WHERE discord_id = %s", (ctx.author.id,))
            current_balance = cursor.fetchone()[0]
            if current_balance is None:
                current_balance = 0
            new_balance = current_balance + coins_earned

            # Update the player's data in the database, including last_work_time
            cursor.execute(
                "UPDATE players SET coins = %s, last_work_time = %s WHERE discord_id = %s",
                (new_balance, current_time, ctx.author.id),
            )
            db.commit()

            # Send the command response with the updated user data
            embed = discord.Embed(
                title="Reborn Legends 🤖",
                description=f"You earned {coins_earned} :coin:! Your new balance is {new_balance} :coin:.",
                color=0x00FF00,
            )
            embed.set_footer(text=f"Total coins earned: {new_balance} coins")
            await ctx.send(embed=embed)
        else:
            # Calculate the remaining cooldown time in hours and minutes
            remaining_cooldown = timedelta(hours=1) - time_difference
            hours, seconds = divmod(remaining_cooldown.total_seconds(), 3600)
            minutes = seconds / 60
            embed = discord.Embed(
                title="Reborn Legends 🤖",
                description=f"You can use this command again in {int(hours)} hours and {int(minutes)} minutes.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)

        print(f"DEBUG: last_work_time: {last_work_time}")
        print(f"DEBUG: current_time: {current_time}")
        print(f"DEBUG: Difference: {time_difference}")
        print(f"DEBUG: Is cooldown reached? {time_difference >= timedelta(hours=1)}")

async def setup(bot):
    await bot.add_cog(work(bot))
