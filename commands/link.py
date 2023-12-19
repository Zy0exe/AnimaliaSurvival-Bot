from functions import *
from import_lib import *

class link(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.steam_api_key = os.getenv("STEAM_API_KEY")

    @commands.command()
    @commands.check(in_animal_shop)
    async def link(self, ctx, steam_id: str = None):
        
        if steam_id is None:
            embed = discord.Embed(
                title="Reborn Legends 🤖",
                description="You need to enter a Steam ID!",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        # Check if steam_id is exactly 17 characters long
        if len(steam_id) != 17 or not steam_id.isdigit():
            embed = discord.Embed(
                title="Reborn Legends 🤖",
                description="Invalid Steam ID format. Steam IDs must be exactly 17 digits long and contain only numbers.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        try:
            url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={self.steam_api_key}&steamids={steam_id}"
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception if the response status is not OK
            data = response.json()
            
            if "response" in data and "players" in data["response"]:
                players = data["response"]["players"]
                
                if len(players) == 0:
                    # No player data found for the provided Steam ID
                    embed = discord.Embed(
                        title="Reborn Legends 🤖",
                        description="No Steam profile found for the provided Steam ID.",
                        color=0xFF0000,
                    )
                    await ctx.send(embed=embed)
                    return

                player = players[0]
                if "steamid" in player:
                    actual_steam_id = player.get("steamid")
                    print(f"Actual Steam ID: {actual_steam_id}")  # Debugging line
                    print(f"Provided Steam ID: {steam_id}")  # Debugging line
                    if actual_steam_id != steam_id:
                        embed = discord.Embed(
                            title="Reborn Legends 🤖",
                            description="The Steam ID does not match a valid Steam account.",
                            color=0xFF0000,
                        )
                        await ctx.send(embed=embed)
                        return

                    # Display player's Steam profile information and prompt for confirmation
                    steam_profile_embed = discord.Embed(
                        title="Steam Profile Confirmation",
                        description=f"Is this your Steam profile?\n\nSteam ID: {steam_id}\nUsername: {player.get('personaname', 'N/A')}\nProfile URL: [link]({player.get('profileurl', 'N/A')})",
                        color=0xFFFF00,
                    )
                    confirmation_message = await ctx.send(embed=steam_profile_embed)

                    # Add reaction options for confirmation
                    await confirmation_message.add_reaction("✅")  # Confirmation emoji
                    await confirmation_message.add_reaction("❌")  # Denial emoji

                    def check(reaction, user):
                        return user == ctx.author and reaction.message.id == confirmation_message.id

                    try:
                        reaction, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)

                        print(str(reaction.emoji))  # Debugging line

                        if str(reaction.emoji) == "✅":
                            # Connect to the database
                            db = mysql.connector.connect(
                                host="localhost", user="root", password="", database="reborn_legends"
                            )

                            # Create a cursor object to interact with the database
                            cursor = db.cursor()

                            # Get the user ID of the person who typed the command
                            discord_id = ctx.author.id

                            # Check if the discord_id already exists in the database
                            cursor.execute("SELECT steam_id, coins_received FROM players WHERE discord_id = %s", (discord_id,))
                            player_data = cursor.fetchone() 
                            
                            # If the discord_id already exists
                            if player_data is not None:
                                existing_steam_id, coins_received = player_data
                                if existing_steam_id == steam_id and coins_received == 0:
                                    # Update the database with the new Steam ID and set coins_received to 1
                                    cursor.execute(
                                        "UPDATE players SET steam_id = %s, coins_received = 1, coins = 75000 WHERE discord_id = %s", (steam_id, discord_id)
                                    )
                                    db.commit()

                                    embed = discord.Embed(
                                        title="Reborn Legends 🤖",
                                        description="Your account has been successfully linked! You received 75,000 coins!",
                                        color=0x00FF00,
                                    )

                                    folder_name = steam_id
                                    folder_path = os.path.join(os.getenv("SERVER_FOLDER_PATH"), folder_name)

                                    if os.path.exists(folder_path):
                                        print(f"Folder '{folder_name}' already exists at path: {folder_path}")
                                        # Optionally, you can add code here to handle the case when the folder already exists

                                    else:
                                        os.makedirs(folder_path, exist_ok=True)
                                        print(f"Folder '{folder_name}' created at path: {folder_path}")

                                    await ctx.send(embed=embed)
                                else:
                                    embed = discord.Embed(
                                        title="Reborn Legends 🤖",
                                        description="Your account is already linked or the Steam ID does not match.",
                                        color=0xFF0000,
                                    )
                                    await ctx.send(embed=embed)

                            # If the discord_id does not exist, create a new row in the database
                            else:
                                cursor.execute(
                                    "INSERT INTO players (discord_id, steam_id, coins_received, coins) VALUES (%s, %s, 1, 75000)",
                                    (discord_id, steam_id),
                                )
                                db.commit()
                                
                                embed = discord.Embed(
                                    title="Reborn Legends 🤖",
                                    description="Your account has been successfully linked! You received 75,000 coins!",
                                    color=0x00FF00,
                                )
                                
                                folder_name = steam_id
                                folder_path = os.path.join(os.getenv("SERVER_FOLDER_PATH"), folder_name)

                                if os.path.exists(folder_path):
                                    print(f"Folder '{folder_name}' already exists at path: {folder_path}")
                                    # Optionally, you can add code here to handle the case when the folder already exists

                                else:
                                    os.makedirs(folder_path, exist_ok=True)
                                    print(f"Folder '{folder_name}' created at path: {folder_path}")
                                
                                await ctx.send(embed=embed)
                            
                            # Close the database connection
                            db.close()

                        elif str(reaction.emoji) == "❌":
                            print("Denial emoji selected")  # Debugging line
                            embed = discord.Embed(
                                title="Reborn Legends 🤖",
                                description="You denied the Steam profile confirmation.",
                                color=0xFF0000,
                            )
                            await ctx.send(embed=embed)
                            return

                        else:
                            print("Unknown emoji selected")  # Debugging line
                            embed = discord.Embed(
                                title="Reborn Legends 🤖",
                                description="Invalid reaction. Please try again.",
                                color=0xFF0000,
                            )
                            await ctx.send(embed=embed)
                            return

                    except asyncio.TimeoutError:
                        embed = discord.Embed(
                            title="Reborn Legends 🤖",
                            description="Steam profile confirmation timed out. Please try again.",
                            color=0xFF0000,
                        )
                        await ctx.send(embed=embed)
                        return

                else:
                    embed = discord.Embed(
                        title="Reborn Legends 🤖",
                        description="The Steam ID does not match a valid Steam account.",
                        color=0xFF0000,
                    )
                    await ctx.send(embed=embed)
                    return

        except requests.exceptions.RequestException as e:
            # Handle network request errors
            embed = discord.Embed(
                title="Reborn Legends 🤖",
                description="An error occurred while communicating with Steam servers.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
        except Exception as e:
            # Handle other errors
            embed = discord.Embed(
                title="Reborn Legends 🤖",
                description=f"Error: {str(e)}",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
        finally:
            # Close the database connection
            if 'db' in locals() and db.is_connected():
                db.close()

async def setup(bot):
    await bot.add_cog(link(bot))
