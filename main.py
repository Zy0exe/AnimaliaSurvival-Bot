from import_lib import *

# ENV
load_dotenv()

TOKEN = os.getenv("TOKEN")

# Connect to the database
db = mysql.connector.connect(
    host="localhost", user="root", password="", database="reborn_legends"
)

bot = commands.Bot(command_prefix="!", help_command=None, intents=discord.Intents.all(), application_id=1100912113867825184)

async def load():
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'commands.{filename[:-3]}')
                print(f'{filename[:-3]} loaded successfully!')
            except Exception as e:
                print(f'{filename} could not be loaded. [{e}]')

async def main():
    await load()
    await bot.start(TOKEN)

async def on_ready():
    await bot.change_presence(activity=discord.Game(name="/help"))
    print('Bot is Online!')

async def on_disconnect():
    await db.close()
    print('Disconnected from database.')

async def on_error(event, *args, **kwargs):
    print(f'An error occurred in {event}. [{args}, {kwargs}]')

async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    embed = discord.Embed(
        title="Animalia Survial 🤖",
        description=f"An error occurred while running the command:\n\n{str(error)}",
        color=0xFF0000,
    )
    await ctx.send(embed=embed)

bot.add_listener(on_ready)
bot.add_listener(on_disconnect)
bot.add_listener(on_error)
bot.add_listener(on_command_error)

@bot.command()
@commands.guild_only()
async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot Shutdown")
        pass