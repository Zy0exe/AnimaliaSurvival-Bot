from functions import *
from import_lib import *

class removecoins(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.superuser = int(os.getenv("SUPER_USER_ID"))
        self.adminrole = int(os.getenv("ADMIN_ROLE_ID"))

    @commands.command()
    async def removecoins(self, ctx, member: discord.Member, amount: int):
        # Check if the user has any of the specified roles
        if not any(role.id in {self.superuser, self.adminrole} for role in ctx.author.roles):
            embed = discord.Embed(
                title="Reborn Legends 🤖",
                description="Insufficient Permissions. You need the required roles to use this command.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        if amount < 0:
            await ctx.send("You cannot remove a negative amount of coins.")
            return

        # Check if the user has linked their Steam ID
        player_data = get_player_data(member.id)
        if player_data is None:
            await ctx.send(f"{member.mention} has not linked their Steam ID, so coins cannot be removed.")
            return

        current_balance = player_data["coins"]
        if current_balance < amount:
            await ctx.send(f"{member.mention} does not have enough coins to remove that amount.")
            return

        new_balance = current_balance - amount
        cursor.execute(
            "UPDATE players SET coins = %s WHERE discord_id = %s",
            (new_balance, member.id),
        )
        db.commit()

        # Fetch the updated user data from the database
        player_data = get_player_data(member.id)

        # Send the command response with the updated user data
        embed = discord.Embed(
            title="Reborn Legends 🤖",
            description=f"{amount} :coin: removed from {member.mention}'s balance. New balance is {player_data['coins']} :coin:.",
            color=0xFF0000,
        )
        await ctx.send(embed=embed)


    @removecoins.error
    async def removecoins_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("Sorry, only admins can use this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please use the command correctly: !removecoins {user} {amount}")
        else:
            await ctx.send(f"An error occurred: {str(error)}")

async def setup(bot):
    await bot.add_cog(removecoins(bot))
