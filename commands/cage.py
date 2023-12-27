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
        player_data = get_player_data(ctx.author.id)
        if not player_data:
            embed = discord.Embed(
                title="Animalia Survival 🤖",
                description=f"{ctx.author.mention}, you need to link your Steam ID first using the !link command.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        player_animals = get_player_animals(ctx.author.id)

        for animal, data in player_animals.items():
            if data.get("quantity", 0) < 0:
                data["quantity"] = 0

        inventory_embed = Embed(title=f"{ctx.author.display_name}'s Cage")
        inventory_embed.add_field(name="Animals", value="\u200b", inline=False)

        if player_animals:
            animal_chunks = list(chunks(list(player_animals.items()), 2))
            for chunk in animal_chunks:
                for animal, data in chunk:
                    if "genders" in data:
                        males, females = 0, 0
                        for gender_data in data["genders"]:
                            gender, quantity = gender_data["gender"], gender_data["quantity"]
                            if gender == "Male":
                                males = quantity
                            elif gender == "Female":
                                females = quantity
                        inventory_embed.add_field(
                            name=f"{animal}{' ' * (25 - len(animal))}",
                            value=f"Male: {males}{' ' * (5 - len(str(males)))}\n Female: {females}{' ' * (3 - len(str(females)))}\n\u200b",
                            inline=True,
                        )
                    else:
                        quantity = data.get('quantity', 'N/A')
                        inventory_embed.add_field(
                            name=f"{animal}{' ' * (25 - len(animal))}",
                            value=f"Quantity: {quantity}{' ' * (5 - len(str(quantity)))}\n\u200b",
                            inline=True,
                        )
                inventory_embed.add_field(
                    name="\u200b", value="\u200b", inline=True
                )
        else:
            inventory_embed.add_field(
                name="Animalia Survival 🤖",
                value="You don't have any animals yet.",
                inline=False,
            )

        await ctx.send(embed=inventory_embed)


async def setup(bot):
    await bot.add_cog(cage(bot))
