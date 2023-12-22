from functions import *
from import_lib import *

class strike_player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.superuser = int(os.getenv("SUPER_USER_ID"))
        self.adminrole = int(os.getenv("ADMIN_ROLE_ID"))

    @commands.hybrid_command(name="strike_player", description="Display server information", with_app_command=True, aliases=['strike'])
    async def strike_player(self, ctx, player: discord.Member = None, *, reason: str = None):
        # Adds a strike to a player's record and bans them if they have 3 strikes.
        # Check if the user invoking the command has the required permissions
        if not any(role.id in {self.superuser, self.adminrole} for role in ctx.author.roles):
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description="Insufficient Permissions. You need the required roles to use this command.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        # Check if the bot has permission to ban members
        if not ctx.guild.me.guild_permissions.ban_members:
            embed = Embed(description="I don't have permission to ban members.")
            return await ctx.send(embed=embed)

        if player is None:
            embed = Embed(description="You need to specify a player to strike!")
            return await ctx.send(embed=embed)

        if player == ctx.author:
            embed = Embed(description="You cannot strike yourself!")
            return await ctx.send(embed=embed)

        if reason is None:
            embed = Embed(description="You need to specify a reason for the strike!")
            return await ctx.send(embed=embed)

        # Get the player's Steam ID from the database
        cursor.execute("SELECT steam_id FROM players WHERE discord_id = %s", (player.id,))
        result = cursor.fetchone()
        if result is None:
            embed = Embed(description="This player is not registered in the database.")
            return await ctx.send(embed=embed)

        steam_id = result[0]

        # Insert the strike into the database
        sql = "INSERT INTO strikes (admin_id, player_steam_id) VALUES (%s, %s)"
        val = (str(ctx.author.id), steam_id)
        cursor.execute(sql, val)
        db.commit()

        # Check the total number of strikes for the player
        cursor.execute(
            "SELECT COUNT(*) FROM strikes WHERE player_steam_id = %s", (steam_id,)
        )
        result = cursor.fetchone()
        strike_count = result[0]

        if strike_count == 3:
            # Ban the player and add their Steam ID to the banlist.txt file
            with open("C:/Reborn Legends/animalia/AnimaliaSurvival/banlist.txt", "a") as f:
                f.write(steam_id + "\n")

            embed = Embed(
                description=f"{player.display_name} has been banned for reaching 3 strikes."
            )
            return await ctx.send(embed=embed)
        else:
            embed = Embed(
                description=f"{player.display_name} has been given a strike. They now have {strike_count} strikes."
            )
            return await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(strike_player(bot))
