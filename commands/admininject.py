from functions import *
from import_lib import *

class ainject(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.superuser = int(os.getenv("SUPER_USER_ID"))
        self.adminrole = int(os.getenv("ADMIN_ROLE_ID"))

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

    @commands.hybrid_command(name="ainject", description="Allows Admins to Inject Animals for players.", with_app_command=True)
    @app_commands.autocomplete(animal=animal_autocomplete)
    @app_commands.autocomplete(gender=gender_autocomplete)
    @app_commands.autocomplete(slot=slot_autocomplete)
    @app_commands.autocomplete(location=location_autocomplete)
    async def ainject(self, ctx, user: discord.User, animal: str = None, gender: str = None, slot: int = None, location: str = None):
        """
        Allows Admins to Inject Animals for players.

        :param user: The user you want to inject the animal for.
        :param animal: The animal you want.
        :param gender: The gender of the animal.
        :param slot: The in-game slot you want.
        :param location: The in-game location you want to spawn.
        """

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

        # Get the animal ID based on the selected gender
        animal_id = self.get_animal_ids(animal, gender)

        # Check if the slot is empty before injecting
        if not await self.is_slot_empty(steam_id, slot):
            confirmation_embed = discord.Embed(
                title="Animalia Survival 🤖",
                description=f"Slot {slot} is not empty. Are you sure you want to inject in this slot?",
                color=discord.Color.yellow(),  # Dark yellow color
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
                description=f"{animal} has been injected into the game for {user.mention} using slot {slot}.",
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

async def setup(bot):
    await bot.add_cog(ainject(bot))