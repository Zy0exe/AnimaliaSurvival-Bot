from functions import *
from import_lib import *
import datetime

webhook_env = os.getenv("PAY_WEBHOOK")

# Add this function for logging transactions
def log_transaction(sender_id, recipient_id, amount, sender_name, recipient_name):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {sender_id} paid {recipient_id} {amount} coins\n"

    with open("transaction_log.txt", "a") as log_file:
        log_file.write(log_entry)


# Add this function for sending transactions to a Discord webhook
def send_to_webhook(sender_id, recipient_id, amount, sender_name, recipient_name):
    webhook_url = webhook_env
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    embed = {
        "title": "Transaction Log",
        "color": 0x00FF00,  # Green color for positive action
        "fields": [
            {"name": "Sender", "value": f"{sender_name} ({sender_id})", "inline": True},
            {"name": "Recipient", "value": f"{recipient_name} ({recipient_id})", "inline": True},
            {"name": "Amount", "value": f"{amount} coins", "inline": True},
        ],
        "timestamp": timestamp,
    }

    payload = {
        "embeds": [embed],
        "username": "Transaction Logger",
    }

    requests.post(webhook_url, json=payload)



class Pay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="pay", description="Pay coins to a user", with_app_command=True)
    @commands.check(in_animal_shop)
    async def pay(self, ctx, member: discord.Member, amount: int):
        """
        Pay coins to a user.

        :param member: The user you want to make the payment to.
        :param amount: The amount you want to send.
        """
        # Check if the amount is valid
        if amount <= 0:
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description="The amount must be greater than 0.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        # Check if the user has enough coins
        sender_data = get_player_data(ctx.author.id)
        if sender_data is None or sender_data["coins"] < amount:
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description="You do not have enough coins to complete this transaction.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return
        
         # Check if the user has a valid entry in the database
        player_data = get_player_data(member.id)
        if player_data is None:
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description="That user hasn't linked their steam profile.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        # Subtract coins from the sender's balance
        cursor.execute(
            "UPDATE players SET coins = coins - %s WHERE discord_id = %s",
            (amount, ctx.author.id),
        )
        db.commit()

        # Add coins to the recipient's balance
        recipient_data = get_player_data(member.id)
        if recipient_data is None:
            save_player_data(member.id)
            recipient_data = get_player_data(member.id)

        cursor.execute(
            "UPDATE players SET coins = coins + %s WHERE discord_id = %s",
            (amount, member.id),
        )
        db.commit()

        # Log the transaction to a file
        log_transaction(ctx.author.id, member.id, amount, ctx.author.name, member.name)

        # Send the transaction to a Discord webhook
        send_to_webhook(ctx.author.id, member.id, amount, ctx.author.name, member.name)


        # Send a confirmation message
        embed = discord.Embed(
            title="Animalia Survial 🤖",
            description=f"You paid {member.mention} {amount} coins.",
            color=0x00FF00,
        )
        await ctx.send(embed=embed)

    @pay.error
    async def pay_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description="Please mention a valid user.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description="Please use the command correctly: !pay {user} {amount}",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description=f"An error occurred: {str(error)}",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Pay(bot))
