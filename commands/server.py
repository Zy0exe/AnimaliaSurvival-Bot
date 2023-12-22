from functions import *
from import_lib import *

class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.servername = os.getenv("SERVER_NAME")
        self.maxplayers = os.getenv("SERVER_MAX_PLAYERS")

    @commands.hybrid_command(name="server", description="Display server information", with_app_command=True, aliases=['sv', 'srv'])
    async def server(self, ctx):
        url = "https://topgameservers.net/api/serverdetails/82039495592270750886131005"

        try:
            response = requests.get(url)
            
            if response.status_code != 200:
                # Request was not successful
                error_message = f"Failed to fetch server information: {response.status_code} {response.reason}"
                embed = discord.Embed(title="Server Information", description=error_message,
                                      color=discord.Color.red())
                await ctx.send(embed=embed)
                return
            
            data = response.text

            if data.lower() == "offline":
                # Server is offline
                server_name = self.servername
                max_players = self.maxplayers
                server_status = "Offline"

                embed = discord.Embed(title="Server Information", color=discord.Color.red())
                embed.add_field(name="Server Name", value=server_name, inline=False)
                embed.add_field(name="Max Players", value=max_players, inline=False)
                embed.add_field(name="Server Status", value=server_status, inline=False)

                await ctx.send(embed=embed)
            else:
                # Server is online, parse the JSON response
                data = response.json()

                if "ServerDetails" not in data:
                    # Invalid response format
                    error_message = "Invalid response format. Failed to fetch server information."
                    embed = discord.Embed(title="Server Information", description=error_message,
                                          color=discord.Color.red())
                    await ctx.send(embed=embed)
                else:
                    server_details = data["ServerDetails"]

                    server_name = server_details.get("Title", "N/A")
                    players_online = server_details.get("Players", "0")
                    max_players = server_details.get("MaxPlayers", "0")
                    server_status = server_details.get("Status", "Unknown")

                    embed = discord.Embed(title="Server Information", color=discord.Color.green())
                    embed.add_field(name="Server Name", value=server_name, inline=False)
                    embed.add_field(name="Players Online", value=f"{players_online}/{max_players}", inline=False)
                    embed.add_field(name="Server Status", value=server_status, inline=False)

                    await ctx.send(embed=embed)

        except requests.exceptions.RequestException as e:
            # Handle any exceptions that occur during the request
            error_message = f"Failed to fetch server information: {str(e)}"
            embed = discord.Embed(title="Server Information", description=error_message,
                                  color=discord.Color.red())
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Server(bot))
