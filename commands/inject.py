from functions import *
from import_lib import *

# @Zyo

class inject(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="inject", description="Inject an animal to a specified slot", with_app_command=True)
    @commands.check(in_animal_shop)
    async def inject(self, ctx, animal: str = None, gender: str = None, slot: int = None):
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

        # Check if the player has linked their Steam ID
        db = mysql.connector.connect(
            host="localhost", user="root", password="", database="reborn_legends"
        )
        cursor = db.cursor()
        discord_id = ctx.author.id
        cursor.execute(
            "SELECT steam_id, animals FROM players WHERE discord_id = %s", (discord_id,)
        )
        player_data = cursor.fetchone()
        if player_data is None or player_data[0] is None:
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description=f"{ctx.author.mention}, you need to link your Steam ID first using the !link command.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        steam_id = player_data[0]

        # Check if the player has the animal
        player_animals = {}
        if player_data[1] is not None:
            try:
                player_animals = json.loads(player_data[1])
            except json.decoder.JSONDecodeError as e:
                traceback.print_exc()
                embed = discord.Embed(
                    title="Animalia Survial 🤖",
                    description=f"{ctx.author.mention}, there was an error decoding your animal data. Please contact an administrator.",
                    color=0xFF0000,
                )
                await ctx.send(embed=embed)
                return

        animal_data = player_animals.get(animal)
        if animal_data is None:
            embed = Embed(description=f"You don't have a {animal}.")
            await ctx.send(embed=embed)
            return

        if not any(
            gender_dict["gender"] == gender for gender_dict in animal_data["genders"]
        ):
            embed = Embed(description=f"You don't have a {gender} {animal}.")
            await ctx.send(embed=embed)
            return

        if animal_data["quantity"] < 1:
            embed = Embed(description=f"You don't have any {animal} left.")
            await ctx.send(embed=embed)
            return

        # Check if the selected gender has a quantity greater than zero
        gender_data = next(
            (gd for gd in animal_data["genders"] if gd["gender"] == gender), None
        )
        if gender_data is None or gender_data["quantity"] <= 0:
            embed = Embed(description=f"You don't have any {gender} {animal} left.")
            await ctx.send(embed=embed)
            return

        # Check if the specified slot is valid
        if slot < 1 or slot > 10:
            embed = Embed(
                description="The specified slot is invalid. Please choose a number between 1 and 10."
            )
            await ctx.send(embed=embed)
            return

        # Inject the animal into the game using the specified slot
        folder_name = os.path.join(os.getenv("SERVER_FOLDER_PATH"))
        player_folder = os.path.join(folder_name, steam_id)
        existing_file = os.path.join(player_folder, f"{steam_id}_{slot-1}.sav")
        if os.path.exists(existing_file):
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description=f"The slot {slot} is already occupied. Do you want to proceed with the injection and lose your animal?",  # @Zyo fair point
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

        # Inject the animal into the game using the specified slot 
        base_path = os.getenv("ANIMAL_TEMPLATES_PATH") #Get the base path from the environment variable
        file_name = f"{base_path}{animal}_{gender}.sav"
        new_file_name = f"{steam_id}_{slot-1}.sav"
        try:
            shutil.copy(file_name, new_file_name)
            print(f"{file_name} copied to {new_file_name}")
        except FileNotFoundError:
            await ctx.send(f"File {file_name} not found.")
            new_file_path = os.path.join(player_folder, new_file_name)
            os.rename(new_file_name, new_file_path)

        # Move the file to the correct folder
        if not os.path.exists(player_folder):
            os.makedirs(player_folder)
        new_file_path = os.path.join(player_folder, new_file_name)
        shutil.move(new_file_name, new_file_path)
        print(f"{new_file_name} moved to {new_file_path}")

        # Subtract one from the quantity of the selected gender in the player's animal data
        for gender_dict in animal_data["genders"]:
            if gender_dict["gender"] == gender:
                gender_dict["quantity"] -= 1

        # Update the player's inventory in the database
        player_animals[animal]["quantity"] -= 1
        player_animals_json = json.dumps(player_animals)
        cursor.execute(
            "UPDATE players SET animals = %s WHERE discord_id = %s",
            (player_animals_json, discord_id),
        )
        db.commit()

        embed = Embed(
            title="Animalia Survial 🤖",
            description=f"{ctx.author.mention} has injected a {animal} into the game using slot {slot}.",
            color=0x00FF00,
        )
        await ctx.send(embed=embed)
        print(f"Animal injected into slot {slot} for player {steam_id}")

async def setup(bot):
    await bot.add_cog(inject(bot))