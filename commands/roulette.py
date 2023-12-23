from functions import *
from import_lib import *

class Roulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.red_black_payout = int(os.getenv("RED_BLACK_PAYOUT", default=2))
        self.green_payout = int(os.getenv("GREEN_PAYOUT", default=10))
        self.allowed_channel_id = int(os.getenv("ROULETTE_CHANNEL_ID"))

    async def check_channel(self, ctx):
        if self.allowed_channel_id != 0 and ctx.channel.id != self.allowed_channel_id:
            not_allowed_embed = discord.Embed(
                title="Channel Restriction",
                description="This command is only allowed in the specified channel.",
                color=0xff0000
            )
            not_allowed_message = await ctx.send(embed=not_allowed_embed)
            return False
        return True
    
    async def betcolor_autocomplete(
        self,
        ctx,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        colours = ['Red', 'Black', 'Green']
        return [
            app_commands.Choice(name=bet_color, value=bet_color)
            for bet_color in colours if current.lower() in bet_color.lower()
        ]
    
    async def betamount_autocomplete(
        self,
        ctx,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        amounts = ['500', '1000', '2000', '3000', '4000', '5000', '6000', '7000', '8000', '9000', '10000']
        return [
            app_commands.Choice(name=bet_amount, value=bet_amount)
            for bet_amount in amounts if current.lower() in bet_amount.lower()
        ]

    @commands.hybrid_command(name="rlt", description="Play roulette!", with_app_command=True, aliases=['roulette'])
    @app_commands.autocomplete(bet_amount=betamount_autocomplete)
    @app_commands.autocomplete(bet_color=betcolor_autocomplete)
    async def roulette(self, ctx, bet_amount: int, bet_color: str):
        bet_color_lower = bet_color.lower()

        if not await self.check_channel(ctx):
            return
        
        # Check if the bet amount is above 100
        if bet_amount <= 100:
            invalid_bet = discord.Embed(
                title="Invalid Bet Amount",
                description="You can only place bets above 100 coins.",
                color=0xff0000
            )
            await ctx.send(embed=invalid_bet)
            return

        # Retrieve user data from your database or storage
        user_data = get_player_data(ctx.author.id)

        if user_data is None:
            no_data = discord.embed(
                title="No Data",
                description="User data not found",
                color=0x3498db
            )
            no_data_message = await ctx.send(embed=no_data)
            return

        # Check if the user has enough coins to place the bet
        if user_data["coins"] < bet_amount or bet_amount <= 0:
            no_coins = discord.embed(
                title="Insufficient Coins",
                description="Invalid bet amount or insufficient coins",
                color=0x3498db
            )
            no_coins_message = await ctx.send(embed=no_coins)
            return

        # Display the spinning animation in an embed
        spin_embed = discord.Embed(
            title="Spinning the Roulette...",
            description="",
            color=0x3498db
        )
        spin_message = await ctx.send(embed=spin_embed)

        # Add a spinning effect
        for _ in range(5):
            await asyncio.sleep(1)

        # Perform the roulette spin
        spin_result = random.choice(["red", "black", "green"])

        # Display the result with emojis in a centered embed
        emoji_map = {"red": "🔴", "black": "⚫", "green": "🟢"}
        result_embed = discord.Embed(
            title="Roulette Result",
            description=f"{' '.join([emoji_map[spin_result]] * 4)}\n"
                        f"🔄 **{spin_result.upper()}** 🔄\n"
                        f"{' '.join([emoji_map[spin_result]] * 4)}",
            color=0x00ff00 if bet_color_lower == spin_result else 0xff0000
        )
        await spin_message.edit(embed=result_embed)
        await asyncio.sleep(2)  # Keep the result display for 2 seconds

        # Check if the user's bet matches the spin result
        if bet_color_lower == spin_result:
            if spin_result == "green":
                winnings = bet_amount * self.green_payout  # Green pays based on the configured ratio
            else:
                winnings = bet_amount * self.red_black_payout  # Red or black pays based on the configured ratio

            user_data["coins"] += winnings
            result_message = f"Congratulations! You won {winnings} coins by betting on {spin_result}!"
        else:
            user_data["coins"] -= bet_amount
            result_message = f"Sorry, you lost {bet_amount} coins. The winning color was {spin_result}."

        # Save the updated user data
        save_player_data(ctx.author.id, user_data)

        # Display the result to the user in a centered embed
        result_embed.description = result_message
        result_embed.set_footer(text=f"Your current balance: {user_data['coins']} coins")
        await ctx.send(embed=result_embed)

async def setup(bot):
    await bot.add_cog(Roulette(bot))
