from functions import *
from import_lib import *

class shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="shop", description="Display Animal Shop", with_app_command=True)
    @commands.check(in_animal_shop)
    async def shop(self, ctx):
        db = mysql.connector.connect(
           host="localhost", user="root", password="", database="animalia_bot"
        )

        cursor = db.cursor()
        cursor.execute("SELECT coins FROM players WHERE discord_id = %s", (ctx.author.id,))
        result = cursor.fetchone()
        if result is not None:
            current_balance = result[0]
        else:
            current_balance = 0

        # Get player's owned animals data
        owned_animals_data = get_player_animals(ctx.author.id)
        owned_animals = (
            "\n ".join(
                [
                    f"{animal.capitalize()} (x{data['quantity']})"
                    for animal, data in owned_animals_data.items()
                ]
            )
            if owned_animals_data
            else ""
        )

        # Shop message
        shop_message = "Available animals for purchase:\n"
        for animal, data in animals.items():
            shop_message += f"{data['image']}{animal}: {data['price']} :coin:\n"

        # Combine the shop message and ephemeral Note embed
        combined_embed = discord.Embed(
            title="Animalia Survial 🤖", description=shop_message, color=0xf1c40f
        )
        combined_embed.add_field(name="Your coins", value=f":coin:`{current_balance}`", inline=False)

        if owned_animals:
            combined_embed.add_field(name="Your owned animals", value=owned_animals, inline=False)

        # Send the combined embed with the ephemeral Note
        await ctx.send(embed=combined_embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(shop(bot))
