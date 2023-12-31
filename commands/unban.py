from functions import *
from import_lib import *
from rcon import rcon

class UnBanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.superuser = int(os.getenv("SUPER_USER_ID"))
        self.adminrole = int(os.getenv("ADMIN_ROLE_ID"))
        self.rcon_host = os.getenv("RCON_ADDRESS")
        self.rcon_port = os.getenv("RCON_PORT")
        self.rcon_passwd = os.getenv("RCON_PW")

    @commands.hybrid_command(name="unban", description="Unban a Player", with_app_command=True)
    @commands.check(in_animal_shop)
    async def unban(self, ctx, steam_id: str):
        """
        Unban a Player.

        :param steam_id: The ID of the player to unban.
        """
        
        if not any(role.id in {self.superuser, self.adminrole} for role in ctx.author.roles):
            embed = discord.Embed(
                title="Animalia Survival 🤖",
                description="Insufficient Permissions. You need the required roles to use this command.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed, ephemeral=True)
            return

        # Ask the admin to confirm the unban
        embed = discord.Embed(
            title="Unban Confirmation",
            description=f"Are you sure you want to unban the player with Steam ID {steam_id}? React with \u2705 to confirm or \u274c to cancel.",
            color=discord.Color.green(),
        )
        confirmation_message = await ctx.send(embed=embed)
        await confirmation_message.add_reaction("\u2705")  # Check mark
        await confirmation_message.add_reaction("\u274c")  # X mark

        # Wait for the admin to react
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["\u2705", "\u274c"]
        reaction, _ = await self.bot.wait_for("reaction_add", check=check)

        # If the admin confirmed the unban, use the Rcon command
        if str(reaction.emoji) == "\u2705":
            rcon_command = f"UnBan.PlayerID {steam_id}"
            response = await rcon(
                rcon_command,
                host=self.rcon_host,
                port=self.rcon_port,
                passwd=self.rcon_passwd
            )

            if "UnBan.PlayerID:UnBan" in response:
                embed = discord.Embed(
                    title="Animalia Survival 🤖",
                    description=f"Player with Steam ID {steam_id} has been unbanned.",
                    color=0x00FF00,
                )
                await ctx.send(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(
                    title="Animalia Survival 🤖",
                    description=f"Failed to unban player with Steam ID {steam_id}. Error: {response}",
                    color=0xFF0000,
                )
                await ctx.send(embed=embed, ephemeral=True)

        # Otherwise, cancel the unban
        else:
            embed = discord.Embed(
                title="Animalia Survival 🤖",
                description=f"Player with Steam ID {steam_id} has not been unbanned.",
                color=0x00FF00,
            )
            await ctx.send(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(UnBanCog(bot))
