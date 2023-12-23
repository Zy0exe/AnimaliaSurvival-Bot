from functions import *
from import_lib import *

class collect(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.collect_cooldown = commands.CooldownMapping.from_cooldown(1, 10800, commands.BucketType.user)
        self.superuser = int(os.getenv("SUPER_USER_ID"))
        self.adminrole = int(os.getenv("ADMIN_ROLE_ID"))
        self.modrole   = int(os.getenv("MOD_ROLE_ID"))
        self.viproleid = int(os.getenv("VIP_ROLE_ID"))
        
    @commands.hybrid_command(name="collect", description="work command for Vips", with_app_command=True)
    @commands.check(in_og_chan)
    async def collect(self, ctx):
        try:
            # Check if the player exists in the database
            player_data = get_player_data(ctx.author.id)
            if player_data is None or player_data.get("steam_id") is None:
                embed = discord.Embed(
                    title="Animalia Survial 🤖",
                    description="You do not exist or have not linked your Steam ID. Please use the !link command to link your Steam account.",
                    color=0xFF0000,
                )
                await ctx.send(embed=embed)
                return

            if not any(role.id in {self.superuser, self.adminrole, self.modrole, self.viproleid} for role in ctx.author.roles):
                embed = discord.Embed(
                    title="Animalia Survial 🤖",
                    description="Insufficient Permissions. You need the required roles to use this command.",
                    color=0xFF0000,
                )
                await ctx.send(embed=embed)
                return

            # Check if the user is on cooldown
            bucket = self.collect_cooldown.get_bucket(ctx.message)
            retry_after = bucket.update_rate_limit()
            if retry_after:
                embed = discord.Embed(
                    title="Animalia Survial 🤖",
                    description=f"You can use this command again in {retry_after:.0f} seconds.",
                    color=0xFF0000,
                )
                await ctx.send(embed=embed)
                return

            # Generate a random amount of coins between 500-2000
            coins_earned = random.randint(350, 2000)

            # Update the user's balance in the database
            db = mysql.connector.connect(
                host="localhost", user="root", password="", database="reborn_legends"
            )
            cursor = db.cursor()
            current_balance = player_data.get("coins", 0)
            new_balance = current_balance + coins_earned
            cursor.execute(
                "UPDATE players SET coins = %s WHERE discord_id = %s",
                (new_balance, ctx.author.id),
            )
            db.commit()
            cursor.close()
            db.close()

            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description=f"You earned {coins_earned} :coin:! Your new balance is {new_balance} :coin:.",
                color=0x00FF00,
            )
            await ctx.send(embed=embed)

        except mysql.connector.Error as e:
            print(f"DEBUG: Error during database query: {e}")
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description="An error occurred while processing your command. Please try again later.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)

    @collect.error
    async def collect_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description=f"You can use this command again in {error.retry_after:.0f} seconds.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(collect(bot))
