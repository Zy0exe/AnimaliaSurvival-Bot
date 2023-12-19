from functions import *
from import_lib import *
import discord

class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.superuser = int(os.getenv("SUPER_USER_ID"))
        self.adminrole = int(os.getenv("ADMIN_ROLE_ID"))
        self.modrole = int(os.getenv("MOD_ROLE_ID"))

    @commands.command(aliases=['id'])
    async def player(self, ctx, member: discord.Member):
        # Check if the user has any of the specified roles
        if not any(role.id in {self.superuser, self.adminrole, self.modrole} for role in ctx.author.roles):
            embed = discord.Embed(
                title="Reborn Legends 🤖",
                description="Insufficient Permissions. You need one of the specified roles to use this command.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        # Check if the user has a valid entry in the database
        player_data = get_player_data(member.id)
        if player_data is None:
            embed = discord.Embed(
                title="Reborn Legends 🤖",
                description="That user does not have a valid entry in the database.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        # Retrieve player's coins and Steam ID
        coins = player_data.get('coins', 0)
        steam_id = player_data.get('steam_id', 'Not available')

        embed = discord.Embed(title="Player Information", color=discord.Color.blue())
        embed.add_field(name="User", value=member.mention, inline=False)
        embed.add_field(name="Steam ID", value=steam_id, inline=False)
        embed.add_field(name="Coins", value=coins, inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Player(bot))
