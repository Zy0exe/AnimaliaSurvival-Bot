from functions import *
from import_lib import *
from rcon import rcon

class announcement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.superuser = int(os.getenv("SUPER_USER_ID"))
        self.rcon_host = os.getenv("RCON_ADDRESS")
        self.rcon_port = os.getenv("RCON_PORT")
        self.rcon_passwd = os.getenv("RCON_PW")

    @commands.hybrid_command(name="announce", description="Make an announcement in-game", with_app_command=True)
    async def announce(self, ctx, text: str = None):
        """
        Make an announcement.

        :param text: What you want to say.
        """
        # Check if the user has permission to use the command
        if not any(role.id in {self.superuser} for role in ctx.author.roles):
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description="Insufficient Permissions. You need the required roles to use this command.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        # Check if there is an actual steam id
        if text is None:
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description="You need to enter some text for the annoucement",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        # Ask the admin to confirm the addition
        embed = discord.Embed(
            title="announcement Confirmation",
            description=f"Are you sure you want to make an announcement with the text: {text}? React with \u2705 to confirm or \u274c to cancel.",
            color=discord.Color.gold(),
        )
        confirmation_message = await ctx.send(embed=embed)
        await confirmation_message.add_reaction("\u2705")  # Check mark
        await confirmation_message.add_reaction("\u274c")  # X mark

        # Wait for the admin to react
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["\u2705", "\u274c"]
        reaction, _ = await self.bot.wait_for("reaction_add", check=check)

        # If the admin confirmed, use the Rcon command to add the Steam ID to the admin list
        if str(reaction.emoji) == "\u2705":
            rcon_command = f"Say {text}"
            response = await rcon(
                rcon_command,
                host=self.rcon_host,
                port=self.rcon_port,
                passwd=self.rcon_passwd
            )

            if F"ServerMessage:{text}" in response:
                embed = discord.Embed(
                    title="Animalia Survial 🤖",
                    description=f"Announcement made.",
                    color=0x2ECC71,
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="Animalia Survial 🤖",
                    description=f"Failed to send the Announcement to the server. Error: {response}",
                    color=0xFF0000,
                )
                await ctx.send(embed=embed)

        # Otherwise, cancel the addition
        else:
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description=f"Annoucement to the server not sent.",
                color=0x00FF00,
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(announcement(bot))
