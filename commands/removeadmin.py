from functions import *
from import_lib import *

class RemoveAdmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.superuser = int(os.getenv("SUPER_USER_ID"))
        self.adminlist_path = os.getenv("ADMINLIST_PATH")

    @commands.command()
    async def removeadmin(self, ctx, discord_id: int = None):
        # Check if the user has any of the specified roles
        if not any(role.id in {self.superuser} for role in ctx.author.roles):
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description="Insufficient Permissions. You need the required roles to use this command.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        # Check if there is an actual discord id
        if discord_id is None:
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description="You need to provide a Discord ID to remove admin access.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        # Check if the player exists in the database
        db = mysql.connector.connect(
            host="localhost", user="root", password="", database="reborn_legends"
        )
        cursor = db.cursor()
        cursor.execute("SELECT steam_id FROM players WHERE discord_id = %s", (discord_id,))
        player_data = cursor.fetchone()
        if player_data is None or player_data[0] is None:
            await ctx.send("This player does not exist or has not linked their Steam ID.")
            return

        # Remove the Steam ID from the "AdminList" text file
        with open(self.adminlist_path, "r") as f:
            admin_list = f.readlines()
        with open(self.adminlist_path, "w") as f:
            for line in admin_list:
                if player_data[0] not in line:
                    f.write(line)
        user = self.bot.get_user(discord_id)
        if user:
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description=f"Admin List {user.mention} has been removed from the admin list.",
                color=0x2ECC71,
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description=f"User with ID {discord_id} has been removed from the admin list.",
                color=0x2ECC71,
            )
            await ctx.send(embed=embed)
        db.close()

async def setup(bot):
    await bot.add_cog(RemoveAdmin(bot))
