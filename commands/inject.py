from functions import *
from import_lib import *

class inject(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def animal_autocomplete(
        self,
        ctx,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        animals = ['Lion', 'Crocodille', 'Elephant', 'Giraffe', 'Hippopotamus', 'Hyena', 'Leopard', 'Meerkat', 'Rhinoceros', 'Wildebeest', 'WildDog', 'Zebra']
        return [
            app_commands.Choice(name=animal, value=animal)
            for animal in animals if current.lower() in animal.lower()
        ]
    
    async def gender_autocomplete(
        self,
        ctx,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        genders = ['Male', 'Female']
        return [
            app_commands.Choice(name=gender, value=gender)
            for gender in genders if current.lower() in gender.lower()
        ]
    
    async def slot_autocomplete(
        self,
        ctx,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        slots = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        return [
            app_commands.Choice(name=slot, value=slot)
            for slot in slots if current.lower() in slot.lower()
        ]

    def get_animal_ids(self, animal: str, gender: str) -> List[str]:
        animals_Males = {
            'Lion': 'Lion_Adult2',
            'Crocodille': 'Crocodille_Adult_M',
            'Elephant': 'Elephant_Adult_M',
            'Giraffe': 'Giraffe_Adult_M', 
            'Hippopotamus': 'Hippopotamus_Adult_M', 
            'Hyena': 'Hyena_Adult_M', 
            'Leopard': 'Leopard_Adult_M', 
            'Meerkat': 'MeerkatAdult_M', 
            'Rhinoceros': 'Rhinoceros_Adult_M', 
            'Wildebeest': 'Wildebeest_Adult_M', 
            'WildDog': 'WildDog_M', 
            'Zebra': 'Zebra_Adult_M',
        }

        animals_Females = {
            'Lion': 'Lioness_Adult',
            'Crocodille': 'Crocodille_Adult_F',
            'Elephant': 'Elephant_Adult_F',
            'Giraffe': 'Giraffe_Adult_F', 
            'Hippopotamus': 'Hippopotamus_Adult_F', 
            'Hyena': 'Hyena_Adult_F', 
            'Leopard': 'Leopard_Adult_F', 
            'Meerkat': 'MeerkatAdult_F', 
            'Rhinoceros': 'Rhinoceros_Adult_F', 
            'Wildebeest': 'Wildebeest_Adult_F', 
            'WildDog': 'WildDog_F', 
            'Zebra': 'Zebra_Adult_F',
        }

        return animals_Males[animal] if gender == 'Male' else animals_Females[animal]

    async def is_slot_empty(self, steam_id: str, slot: int) -> bool:
        """
        Check if the specified slot is empty.
        """
        rcon_command = f"PlayerSlot {steam_id} {slot - 1}"
        response = await rcon(
            rcon_command,
            host=os.getenv("RCON_ADDRESS"),
            port=os.getenv("RCON_PORT"),
            passwd=os.getenv("RCON_PW")
        )
        return f"PlayerSlot:{steam_id}:SlotNotFound" in response
    
    async def location_autocomplete(
        self,
        ctx,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        locations = {
            'South': {'x': -200365, 'y': 70810, 'z': 3177},
            'East': {'x': -6567, 'y': 159572, 'z': 4297},
            'East': {'x': -60525, 'y': -165321, 'z': 13620},
            'Northwest': {'x': 111844, 'y': -122014, 'z': 7860},
            'Northeast': {'x': 102393, 'y': 86158, 'z': 6283},
            'Southeast': {'x': -148784.0, 'y': 124121.0, 'z': 3177.0},
            'Southwest': {'x': -180000.0, 'y': -136600.0, 'z': 5800.0},
            'Region 0': {'x': 1035.0, 'y': 29318.0, 'z': 4468.0},
            'North': {'x': 105446, 'y': 3836, 'z': 6311},
        }
        return [
            app_commands.Choice(name=spawn_name, value=spawn_name)
            for spawn_name in locations.keys() if current.lower() in spawn_name.lower()
        ]

    @commands.hybrid_command(name="inject", description="Inject an animal to a specified slot", with_app_command=True)
    @commands.check(in_animal_shop)
    @app_commands.autocomplete(animal=animal_autocomplete)
    @app_commands.autocomplete(gender=gender_autocomplete)
    @app_commands.autocomplete(slot=slot_autocomplete)
    @app_commands.autocomplete(location=location_autocomplete)
    async def inject(self, ctx, animal: str = None, gender: str = None, slot: int = None, location: str = None):
        """
        Inject a animal into a specified slot.

        :param animal: The animal you want.
        :param gender: The gender of the animal.
        :param slot: TThe in-game slot you want.
        :param location: The in-game location you want to spawn.
        """

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
            host="localhost", user="root", password="", database="animalia_bot"
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

        animal_id = self.get_animal_ids(animal, gender)

        if not await self.is_slot_empty(steam_id, slot):
            confirmation_embed = discord.Embed(
                title="Animalia Survival 🤖",
                description=f"Slot {slot} is not empty. Are you sure you want to inject in this slot?",
                color=discord.Color.yellow(),
            )
            confirmation_embed.set_footer(text="Confirmation Process")
            confirmation_message = await ctx.send(embed=confirmation_embed)
            
            # Add the confirmation reactions to the message
            await confirmation_message.add_reaction("✅")
            await confirmation_message.add_reaction("❌")
            
            try:
                reaction, _ = await self.bot.wait_for(
                    "reaction_add",
                    check=lambda r, u: u == ctx.author and r.message.id == confirmation_message.id and str(r.emoji) in ["✅", "❌"],
                    timeout=30.0  # 30 seconds timeout
                )
            except asyncio.TimeoutError:
                # Handle timeout (admin didn't react in time)
                await confirmation_message.delete()
                return
            
            if str(reaction.emoji) == "❌":
                await confirmation_message.delete()
                cancel_embed = discord.Embed(
                    title="Animalia Survival 🤖",
                    description="Animal injection canceled.",
                    color=0xFFD700,  # You can use a different color for the cancel message
                )
                cancel_embed.set_footer(text="Injection Canceled")
                await ctx.send(embed=cancel_embed, delete_after=10)
                return

        if location:
            locations = {
                'South': {'x': -200365, 'y': 70810, 'z': 3177},
                'East': {'x': -6567, 'y': 159572, 'z': 4297},
                'West': {'x': -60525, 'y': -165321, 'z': 13620},
                'Northwest': {'x': 111844, 'y': -122014, 'z': 7860},
                'Northeast': {'x': 102393, 'y': 86158, 'z': 6283},
                'Southeast': {'x': -148784.0, 'y': 124121.0, 'z': 3177.0},
                'Southwest': {'x': -180000.0, 'y': -136600.0, 'z': 5800.0},
                'Region 0': {'x': 1035.0, 'y': 29318.0, 'z': 4468.0},
                'North': {'x': 105446, 'y': 3836, 'z': 6311},
            }

            if location not in locations:
                await ctx.send(f"Invalid location: {location}.")
                return

            x, y, z = locations[location]['x'], locations[location]['y'], locations[location]['z']
        else:
            x, y, z = -180000.0, -136600.0, 5800.0

        # Inject the animal into the game using the specified slot
        rcon_command = f"CreateSaveSlot {steam_id} {animal_id} {slot-1} 1 1 1 1 1 1 1 1 1 {x} {y} {z} 185"
        response = await rcon(
            rcon_command,
            host=os.getenv("RCON_ADDRESS"),
            port=os.getenv("RCON_PORT"),
            passwd=os.getenv("RCON_PW")
        )
        print(response)

        # Handle the Rcon response as needed
        if f"CreateSaveSlot:CreateAnimalInSlot:{steam_id}:{slot-1}" in response:
            success_embed = discord.Embed(
                title="Animalia Survival 🤖",
                description=f"{animal} has been injected into the game on the slot {slot}.",
                color=0x00FF00,
            )
            success_embed.set_footer(text="Injection successful")
            await ctx.send(embed=success_embed)
            print(f"Animal injected into slot {slot} for player {steam_id}")
            print(response)
        else:
            failure_embed = discord.Embed(
                title="Animalia Survival 🤖",
                description="Failed to inject animal. Please check the logs for details.",
                color=0xFF0000,
            )
            failure_embed.set_footer(text="Injection failed")
            await ctx.send(embed=failure_embed)
            print(f"Failed to inject animal into slot {slot} for player {steam_id}")

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

async def setup(bot):
    await bot.add_cog(inject(bot))