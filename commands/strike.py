from functions import *
from import_lib import *
import datetime

class strike_player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.superuser = int(os.getenv("SUPER_USER_ID"))
        self.adminrole = int(os.getenv("ADMIN_ROLE_ID"))
        self.strike_chat = os.getenv("STRIKE_CHAT")
        self.rcon_host = os.getenv("RCON_ADDRESS")
        self.rcon_port = os.getenv("RCON_PORT")
        self.rcon_passwd = os.getenv("RCON_PW")
        self.webhook = os.getenv("STRIKEBAN_WEBHOOK")

    async def send_strike_message(self, player):
        print("Strike channel ID:", self.strike_chat)
        channel_id = int(self.strike_chat)
        strike_channel = self.bot.get_channel(channel_id)

        if strike_channel:
            print("Strike channel:", strike_channel)

            embed = discord.Embed(
                title="Strike Report",
                description=(
                    f"{player.mention},\n\n"
                    f"{player.display_name} / {player.id} you have been reported to staff for a rule violation.\n"
                    f"To appeal this strike, have your recordings ready and [open a Blue Ticket](https://discord.com/channels/1181029094822006857/1183107878924583064).\n\n"
                    f"All strikes are appealable, but you must do so within 48hrs.\n\n"
                    f"Strikes fall off after 14 days.\n\n"
                ),
                color=0xFF0000, 
            )

            await strike_channel.send(embed=embed)
        else:
            print("Strike channel not found")
    
    def send_to_webhook(self, player_banned, playerbanned_id):
            webhook_url = self.webhook
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            embed = {
                "title": "Ban Log",
                "color": 0xFF0000,  # Red color for ban action
                'description': f"The user {player_banned} with Steam ID {playerbanned_id} has been banned for reaching for strikes.",
                "timestamp": timestamp,
            }

            payload = {
                "embeds": [embed],
                "username": "Ban Logger",
            }

            requests.post(webhook_url, json=payload)

    @commands.hybrid_command(name="strike", description="Strike a Player.", with_app_command=True)
    async def strike_player(self, ctx, player: discord.Member = None, *, reason: str = None):
        """
        Strike a Player.

        :param player: user to warn.
        :param reason: the reason of the warning.
        """
        if not any(role.id in {self.superuser, self.adminrole} for role in ctx.author.roles):
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description="Insufficient Permissions. You need the required roles to use this command.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        # Check if the bot has permission to ban members
        if not ctx.guild.me.guild_permissions.ban_members:
            embed = Embed(description="I don't have permission to ban members.")
            return await ctx.send(embed=embed)

        if player is None:
            embed = Embed(description="You need to specify a player to strike!")
            return await ctx.send(embed=embed)

        if player == ctx.author:
            embed = Embed(description="You cannot strike yourself!")
            return await ctx.send(embed=embed)

        if reason is None:
            embed = Embed(description="You need to specify a reason for the strike!")
            return await ctx.send(embed=embed)

        # Get the player's Steam ID from the database
        cursor.execute("SELECT steam_id FROM players WHERE discord_id = %s", (player.id,))
        result = cursor.fetchone()
        if result is None:
            embed = Embed(description="This player is not registered in the database.")
            return await ctx.send(embed=embed)

        steam_id = result[0]

        # Insert the strike into the database
        sql = "INSERT INTO strikes (admin_id, player_steam_id) VALUES (%s, %s)"
        val = (str(ctx.author.id), steam_id)
        cursor.execute(sql, val)
        db.commit()

        # Check the total number of strikes for the player
        cursor.execute(
            "SELECT COUNT(*) FROM strikes WHERE player_steam_id = %s", (steam_id,)
        )
        result = cursor.fetchone()
        strike_count = result[0]

        # Send a strike message to the specified channel
        await self.send_strike_message(player)

        if strike_count == 3:
            rcon_command = f"Ban.PlayerID {steam_id}"

            # Execute the Rcon command
            response = await rcon(
                rcon_command,
                host=self.rcon_host,
                port=self.rcon_port,
                passwd=self.rcon_passwd
            )

            # Check the response from Rcon
            if "Ban.PlayerID:Ban" in response:
                self.send_to_webhook(
                    player.display_name,
                    steam_id,
                )
                Banned_embed = discord.Embed(
                    title="Animalia Survival 🤖",
                    description=f"Player with Steam ID {steam_id} has been banned for reaching 3 strikes.",
                    color=0x00FF00,
                )
                Banned_embed.set_footer(text="Player Banned")
                await ctx.send(embed=Banned_embed, ephemeral=True)
            else:
                Error_embed = discord.Embed(
                    title="Animalia Survival 🤖",
                    description=f"Failed to ban player with Steam ID {steam_id}. Error: {response}",
                    color=0xFF0000,
                )
                Error_embed.set_footer(text="rcon error contact bot developer")
                await ctx.send(embed=Error_embed, ephemeral=True)
        else:
            # If the player doesn't reach 3 strikes, inform about the strike count
            embed = discord.Embed(
                description=f"{player.display_name} has been given a strike. They now have {strike_count} strikes.",
                color=0x00FF00,
            )
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(strike_player(bot))
