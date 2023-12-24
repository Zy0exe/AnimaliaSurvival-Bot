from import_lib import *

class GameServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.server_address = os.getenv("RCON_ADDRESS")
        self.server_port = os.getenv("RCON_PORT")
        self.rcon_password = os.getenv("RCON_PW")

    async def rcon(self, rcon_command):
        try:
            response = await rcon(
                rcon_command, host=self.server_address, port=self.server_port, passwd=self.rcon_password)
            return response
        except Exception as e:
            print(f"Error communicating with the server: {e}")
            return f"Error communicating with the server: {e}"

    async def rcon_command_autocomplete(
        self,
        ctx,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        rcon_commands = {
            'Help',
            'Say',
            'Time',
            'Day',
            'Night',
            'tp.PlayerID',
            'tp.All',
            'GetServerName',
            'GetServerSettings',
        }
        return [
            app_commands.Choice(name=rcon_command, value=rcon_command)
            for rcon_command in rcon_commands if current.lower() in rcon_command.lower()
        ]

    @commands.hybrid_command(name="rcon", description="Execute In-game commands", with_app_command=True)
    @app_commands.autocomplete(rcon_command=rcon_command_autocomplete)
    async def rcon_command(self, ctx, *, rcon_command: str):
        try:
            response = await self.rcon(rcon_command)
            print(response)

            if response:
                embed = discord.Embed(
                    title="Animalia Survival 🤖",
                    description=f"Response from server: {response}",
                    color=0x00FF00,
                )
                await ctx.send(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(
                    title="Animalia Survival 🤖",
                    description=f"Command '{rcon_command}' executed.",
                    color=0x00FF00,
                )
                await ctx.send(embed=embed, ephemeral=True)
        except Exception as e:
            print(f"Error communicating with the server: {e}")
            embed = discord.Embed(
                title="Animalia Survival",
                description=f"Error communicating with the server: {e}",
                color=0xFF0000,
            )
            await ctx.send(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(GameServer(bot))
