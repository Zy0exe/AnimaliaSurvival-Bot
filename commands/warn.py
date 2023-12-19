from functions import *
from import_lib import *
from .strike import strike_player

class warn_player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.superuser = int(os.getenv("SUPER_USER_ID"))
        self.adminrole = int(os.getenv("ADMIN_ROLE_ID"))
        self.modrole   = int(os.getenv("MOD_ROLE_ID"))

    @commands.command(name="warn")
    async def warn_player(self, ctx, player: discord.Member = None, *, reason: str = None):

        if not any(role.id in {self.superuser, self.adminrole} for role in ctx.author.roles):
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description="Insufficient Permissions. You need the required roles to use this command.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        if player is None:
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description="You need to specify a player to warn!",
                color=0x2ECC71,
            )
            return await ctx.send(embed=embed)

        if player == ctx.author:
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description="You cannot warn yourself",
                color=0x2ECC71,
            )
            return await ctx.send(embed=embed)

        if reason is None:
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description="You need to specify a reason for the warning!",
                color=0x2ECC71,
            )
            return await ctx.send(embed=embed)

        # Check if the player is already banned
        banlist_path = os.getenv("BANLIST_PATH")

        with open(banlist_path, "r") as f:
            banned_players = [line.strip() for line in f.readlines()]
        if str(player.id) in banned_players:
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description=f"{player.mention} is already banned!",
                color=0x2ECC71,
            )
            return await ctx.send(embed=embed)

        # Insert warning into the database
        sql = "INSERT INTO warnings (player_id, reason, warning_date) VALUES (%s, %s, %s)"
        val = (str(player.id), reason, (datetime.today()).date())
        cursor.execute(sql, val)
        db.commit()

        # Get the number of warnings the player has
        cursor.execute(
            "SELECT COUNT(*) FROM warnings WHERE player_id = %s", (str(player.id),)
        )
        num_warnings = cursor.fetchone()[0]

        # Check if the player has reached the warning limit
        if num_warnings >= 3:
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description=f"{player.mention} has reached the maximum number of warnings! They will now receive a strike.",
                color=0xE74C3C,  # Red color
            )
            await ctx.invoke(self.bot.get_command('strike'), player=player, reason="Received 3 warnings.")
            cursor.execute("DELETE FROM warnings WHERE player_id = %s", (str(player.id),))
            db.commit()
        else:
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description=f"{player.mention} has been warned | Reason: {reason}. They now have {3 - num_warnings} warning(s) remaining.",
                color=0x2ECC71,
            )
            return await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(warn_player(bot))
