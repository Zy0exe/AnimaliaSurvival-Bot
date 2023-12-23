from functions import *
from import_lib import *

class ainject(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.superuser = int(os.getenv("SUPER_USER_ID"))
        self.adminrole = int(os.getenv("ADMIN_ROLE_ID"))

    @commands.hybrid_command(name="ainject", description="Allows Admins to Inject Animals for players.", with_app_command=True)
    async def ainject(self, ctx, user: discord.User, animal: str = None, gender: str = None, slot: int = None):
        # Check if the user has any of the specified roles
        if not any(role.id in {self.superuser, self.adminrole} for role in ctx.author.roles):
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description="Insufficient Permissions. You need the required roles to use this command.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return
        
        if animal is None:
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description="You need to specify an animal to inject.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        if gender is None:
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description="You need to specify a gender for the animal.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        if slot is None:
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description="You need to specify a slot to inject the animal in.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        # Retrieve the Discord ID of the mentioned user
        discord_id = user.id
        
        player_data = get_player_data(discord_id)  # Replace with your own method to retrieve player data
       
        # Check if the player data exists
        if player_data is None:
            await ctx.send(f"{user.mention} has not linked their Steam ID.")
            return

        # Retrieve the Steam ID associated with the Discord ID
        steam_id = player_data["steam_id"]


        # Inject the animal into the game using the specified slot
        base_path = os.getenv("ANIMAL_TEMPLATES_PATH")
        folder_name = os.path.join(os.getenv("SERVER_FOLDER_PATH"))
        file_name = f"{base_path}{animal}_{gender}.sav"
        player_folder = os.path.join(folder_name, steam_id)
        new_file_name = f"{steam_id}_{slot-1}.sav"
        new_file_path = os.path.join(player_folder, new_file_name)

        # Check if the specified slot is valid
        if slot < 1 or slot > 10:
            embed = Embed(
                description="The specified slot is invalid. Please choose a number between 1 and 10."
            )
            await ctx.send(embed=embed)
            return

        if os.path.exists(new_file_path):
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description=f"The slot {slot} is already occupied. Do you want to proceed with the injection and overwrite the existing animal data?",
                color=0xFF0000,
            )
            confirmation_msg = await ctx.send(embed=embed)
            await confirmation_msg.add_reaction("✅")  # Add a checkmark reaction to confirm
            await confirmation_msg.add_reaction("❌")  # Add a cross reaction to cancel

            def check(reaction, user):
                return (
                    user == ctx.author
                    and str(reaction.emoji) in ["✅", "❌"]
                    and reaction.message.id == confirmation_msg.id
                )

            try:
                reaction, _ = await ctx.bot.wait_for(
                    "reaction_add", timeout=60, check=check
                )
            except asyncio.TimeoutError:
                embed = discord.Embed(
                    title="Animalia Survial 🤖",
                    description="Confirmation timed out.",
                    color=0xFF0000,
                )
                await ctx.send(embed=embed)
                return

            if str(reaction.emoji) == "❌":
                embed = discord.Embed(
                    title="Animalia Survial 🤖",
                    description="Injection canceled.",
                    color=0xFF0000,
                )
                await ctx.send(embed=embed)
                return

        try:
            shutil.copy(file_name, new_file_path)
            print(f"{file_name} copied to {new_file_path}")
        except FileNotFoundError:
            await ctx.send(f"File {file_name} not found.")
            return

        embed = Embed(
            title="Animalia Survial 🤖",
            description=f"{animal} has been injected into the game for {user.mention} using slot {slot}.",
            color=0x00FF00,
        )
        await ctx.send(embed=embed)
        print(f"Animal injected into slot {slot} for player {steam_id}")

async def setup(bot):
    await bot.add_cog(ainject(bot))