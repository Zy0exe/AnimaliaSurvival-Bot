from functions import *
from import_lib import *
from itertools import islice

# Define the chunks function to split a list into smaller chunks
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

class cage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.check(in_animal_shop)
    @commands.hybrid_command(name="cage", description="Shows your cage", with_app_command=True)
    async def cage(self, ctx):
        # Retrieve player data from the database
        player_data = get_player_data(ctx.author.id)
        if not player_data:
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description=f"{ctx.author.mention}, you need to link your Steam ID first using the !link command.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        # Retrieve player's animal inventory from the database
        player_animals = get_player_animals(ctx.author.id)

        # Fix negative quantities
        for animal, data in player_animals.items():
            if data.get("quantity", 0) < 0:
                data["quantity"] = 0

        # Generate the inventory message
        inventory_embed = Embed(title=f"{ctx.author.display_name}'s cage")
        inventory_embed.add_field(name="Animals", value="\u200b", inline=False)

        if player_animals:
            animal_chunks = list(chunks(list(player_animals.items()), 2))
            for chunk in animal_chunks:
                for animal, data in chunk:
                    # Add animal's genders if specified
                    if "genders" in data:
                        males = 0
                        females = 0
                        for gender_data in data["genders"]:
                            gender = gender_data["gender"]
                            quantity = gender_data["quantity"]
                            if gender == "M":
                                males = quantity
                            elif gender == "F":
                                females = quantity
                        inventory_embed.add_field(
                            name=f"{animal}{' ' * (25 - len(animal))}",
                            value=f"Male: {males}{' ' * (5 - len(str(males)))}\nFemale: {females}{' ' * (3 - len(str(females)))}\n\u200b",
                            inline=True,
                        )
                    else:
                        # If animal has no genders specified, show total quantity
                        inventory_embed.add_field(
                            name=f"{animal}{' ' * (25 - len(animal))}",
                            value=f"Quantity: {data.get('quantity', 'N/A')}{' ' * (5 - len(str(data.get('quantity', 'N/A'))))}\n\u200b",
                            inline=True,
                        )
                inventory_embed.add_field(
                    name="\u200b", value="\u200b", inline=True
                ) # add an empty field to separate rows
        else:
            inventory_embed.add_field(
                name="Animalia Survial 🤖",
                value="You don't have any animals yet.",
                inline=False,
            )

        await ctx.send(embed=inventory_embed)


async def setup(bot):
    await bot.add_cog(cage(bot))
