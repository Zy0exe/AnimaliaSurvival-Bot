from functions import *
from import_lib import *

class clearcage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.superuser = int(os.getenv("SUPER_USER_ID"))
        self.adminrole = int(os.getenv("ADMIN_ROLE_ID"))

    @commands.hybrid_command(name="clearcage", description="clears the cage of a player (Admin Only)", with_app_command=True)
    async def clearcage(self, ctx, user: discord.Member):

        if not any(role.id in {self.superuser, self.adminrole} for role in ctx.author.roles):
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description="Insufficient Permissions. You need the required roles to use this command.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return
        
        if clear_player_animals(user.id):
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description=f"{user.mention}'s animal inventory has been cleared!",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description=f"{user.mention} needs to link their Steam ID first using the !link command.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(clearcage(bot))
