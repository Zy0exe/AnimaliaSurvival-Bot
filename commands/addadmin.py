from functions import *
from import_lib import *

class addadmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.superuser = int(os.getenv("SUPER_USER_ID"))
        self.adminlist_path = os.getenv("ADMINLIST_PATH")

    @commands.command()
    @commands.has_role(1101301737761030205)
    async def addadmin(self, ctx, discord_id: int = None):
        # Check if the user has permission to use the command
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
                description="You need to provide a Discord ID to give admin access.",
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
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description="This player does not exist or has not linked their Steam ID.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        # Add the Steam ID to the "AdminList" text file
        with open(self.adminlist_path, "a") as f:
            f.write(player_data[0] + "\n")
        user = await self.bot.fetch_user(discord_id)
        if user:
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description=f"Admin List {user.mention} | has been added to the admin list.",
                color=0x2ECC71,
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description=f"User with ID {discord_id} has been added to the admin list.",
                color=0x2ECC71,
            )
            await ctx.send(embed=embed)
        db.close()

async def setup(bot):
    await bot.add_cog(addadmin(bot))
