from functions import *
from import_lib import *
from rcon import rcon

class TpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.superuser = int(os.getenv("SUPER_USER_ID"))
        self.adminrole = int(os.getenv("ADMIN_ROLE_ID"))
        self.tp_enabled = os.getenv("TP_ENABLED", "True").lower() == "true"

    async def is_tp_allowed(self, ctx):
        if not self.tp_enabled:
            if not any(role.id in {self.superuser, self.adminrole} for role in ctx.author.roles):
                embed = discord.Embed(
                    title="Animalia Survival 🤖",
                    description="Teleportation is currently disabled. Only superusers and users with admin role can use this command.",
                    color=0xFF0000,
                )
                await ctx.send(embed=embed, ephemeral=True)
                return False
        return True

    @commands.hybrid_command(name="tp", description="Teleports a player to specified coordinates", with_app_command=True)
    @commands.check(in_animal_shop)
    async def tp(self, ctx, player_id: str, x: float, y: float, z: float):
        """
        Teleports a player to specified coordinates.

        :param player_id: The ID of the player to teleport.
        :param x: The X-coordinate to teleport the player to.
        :param y: The Y-coordinate to teleport the player to.
        :param z: The Z-coordinate to teleport the player to.
        """
         
        if not await self.is_tp_allowed(ctx):
            return

        # Ask the admin to confirm the teleport
        embed = discord.Embed(
            title="Teleport Confirmation",
            description=f"Are you sure you want to teleport the player with ID {player_id} to coordinates ({x}, {y}, {z})? React with \u2705 to confirm or \u274c to cancel.",
            color=discord.Color.blue(),
        )
        confirmation_message = await ctx.send(embed=embed)
        await confirmation_message.add_reaction("\u2705")  # Check mark
        await confirmation_message.add_reaction("\u274c")  # X mark

        # Wait for the admin to react
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["\u2705", "\u274c"]
        reaction, _ = await self.bot.wait_for("reaction_add", check=check)

        # If the admin confirmed the teleport, use the Rcon command
        if str(reaction.emoji) == "\u2705":
            rcon_command = f"tp.PlayerID {player_id} {x} {y} {z}"
            response = await rcon(
                rcon_command,
                host=os.getenv("RCON_ADDRESS"),
                port=os.getenv("RCON_PORT"),
                passwd=os.getenv("RCON_PW")
            )

            if "tp.PlayerID:TeleportedPlayer" in response:
                embed = discord.Embed(
                    title="Animalia Survival 🤖",
                    description=f"Player with ID {player_id} has been teleported to ({x}, {y}, {z}).",
                    color=0x00FF00,
                )
                await ctx.send(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(
                    title="Animalia Survival 🤖",
                    description=f"Failed to teleport player with ID {player_id}. Error: {response}",
                    color=0xFF0000,
                )
                await ctx.send(embed=embed, ephemeral=True)

        # Otherwise, cancel the teleport
        else:
            embed = discord.Embed(
                title="Animalia Survival 🤖",
                description=f"Player with ID {player_id} has not been teleported.",
                color=0x00FF00,
            )
            await ctx.send(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(TpCog(bot))
