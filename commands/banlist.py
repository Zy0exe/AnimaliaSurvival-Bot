import asyncio
from functions import *
from import_lib import *
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class BanListHandler(FileSystemEventHandler):
    def __init__(self, cog, file_path, channel_id):
        super().__init__()
        self.cog = cog
        self.file_path = file_path
        self.channel_id = channel_id

    def on_modified(self, event):
        if event.src_path == self.file_path:
            asyncio.create_task(self.cog.send_banlist_update())

class banlist(commands.Cog):
    def __init__(self, bot, file_path, channel_id, delete_emoji):
        self.bot = bot
        self.file_path = file_path
        self.channel_id = channel_id
        self.banlist_handler = BanListHandler(self, file_path, channel_id)
        self.observer = Observer()
        self.observer.schedule(self.banlist_handler, path=file_path, recursive=False)
        self.observer.start()

        self.superuser = int(os.getenv("SUPER_USER_ID"))
        self.adminrole = int(os.getenv("ADMIN_ROLE_ID"))
        self.delete_emoji = delete_emoji

    async def send_banlist_update(self):
        try:
            with open(self.file_path, "r") as file:
                ban_list = file.read()
        except FileNotFoundError:
            print("The ban list file was not found.")
            return
        except Exception as e:
            print(f"An error occurred while reading the ban list: {e}")
            return

        if ban_list:
            channel = self.bot.get_channel(self.channel_id)
            if channel is not None:
                embed = discord.Embed(
                    title="Ban List Update",
                    description=ban_list,
                    color=0xFF0000
                )
                try:
                    await channel.send(embed=embed)
                except discord.HTTPException as ex:
                    print(f"Error sending ban list update: {ex}")
            else:
                print(f"Channel with ID {self.channel_id} not found.")
        else:
            print("The ban list is empty.")

    @commands.command()
    async def banlist(self, ctx):

        if not any(role.id in {self.superuser, self.adminrole} for role in ctx.author.roles):
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description="Insufficient Permissions. You need the required roles to use this command.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        allowed_channel_id = 1183107878924583064  # Replace with the actual ID of the allowed channel
        if ctx.channel.id != allowed_channel_id:
            embed = discord.Embed(
                title="Animalia Survial 🤖",
                description="This command can only be used in the specified text channel.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        try:
            with open(self.file_path, "r") as file:
                ban_list = file.read().splitlines()
        except FileNotFoundError:
            embed = discord.Embed(
                title="Error",
                description="The ban list file was not found.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
            return
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"An error occurred while reading the ban list: {e}",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
            return

        if not ban_list:
            embed = discord.Embed(
                title="Information",
                description="The ban list is empty.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
            return

        page_size = 20  # Set the number of entries per page
        total_pages = (len(ban_list) + page_size - 1) // page_size

        page = 1
        start_index = (page - 1) * page_size
        end_index = page * page_size

        embed = discord.Embed(
            title=f"Ban List (Page {page}/{total_pages})",
            description="\n".join(ban_list[start_index:end_index]),
            color=0xFF0000
        )

        message = await ctx.send(embed=embed)

        if total_pages > 1:
            reactions = ["⬅️", "➡️", self.delete_emoji]

            for reaction in reactions:
                await message.add_reaction(reaction)

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in reactions

            while True:
                try:
                    reaction, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)

                    if str(reaction.emoji) == "⬅️" and page > 1:
                        page -= 1
                    elif str(reaction.emoji) == "➡️" and page < total_pages:
                        page += 1
                    elif str(reaction.emoji) == self.delete_emoji:
                        await message.delete()
                        break  # Exit the loop if the delete reaction is used
                    else:
                        break  # Exit the loop if an invalid reaction is received

                    start_index = (page - 1) * page_size
                    end_index = page * page_size

                    embed.title = f"Ban List (Page {page}/{total_pages})"
                    embed.description = "\n".join(ban_list[start_index:end_index])

                    await message.edit(embed=embed)

                except asyncio.TimeoutError:
                    break  # Exit the loop if no reaction is received within the timeout

        self.observer.stop()
        self.observer.join()

async def setup(bot):
    file_path = os.getenv("BANLIST_PATH")
    channel_id = 1183107878924583064  # Replace with the actual ID of the Discord channel
    delete_emoji = "❌"  # Replace with the desired delete emoji
    cog = banlist(bot, file_path, channel_id, delete_emoji)
    await cog.send_banlist_update()  # Send the initial ban list
    await bot.add_cog(cog)
