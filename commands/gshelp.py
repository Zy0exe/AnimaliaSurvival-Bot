from import_lib import *

class GameServer(commands.Cog):
    def __init__(self, bot, server_address, server_port, rcon_password):
        self.bot = bot
        self.server_address = server_address
        self.server_port = server_port
        self.rcon_password = rcon_password

    @commands.command(name='gshelp')
    async def gshelp(self, ctx):
        help_message = "This is the Game Server Help Command. Use !rcon <command> to send RCON commands to the game server."
        await ctx.send(help_message)

    @commands.hybrid_command(name="rcon", description="Execute In-game commands", with_app_command=True)
    async def rcon_command(self, ctx, *, rcon_command: str):
        try:
            # Connect to the server
            response = await rcon(
            rcon_command, host=self.server_address, port=self.server_port, passwd=self.rcon_password)
            
            # Extract the relevant information from the response
            response_text = response.split(':', 1)[1].strip() if ':' in response else None

            if response_text:
                embed = discord.Embed(
                    title="Animalia Survival 🤖",
                    description=f"Response from server: {response_text}",
                    color=0xFF0000,
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="Animalia Survival 🤖",
                    description=f"Command '{rcon_command}' executed.",
                    color=0xFF0000,
                )
                await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error communicating with the server: {e}")
            await ctx.send(f"Error communicating with the server: {e}")

async def setup(bot):
    # Replace these values with your actual game server information
    server_address = "161.97.78.125"
    server_port = 31001
    rcon_password = "2002"
    
    await bot.add_cog(GameServer(bot, server_address, server_port, rcon_password))
