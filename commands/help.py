from functions import *
from import_lib import *

class HelpMenu(menus.ListPageSource):
    def __init__(self, ctx, data, admin=False):
        self.ctx = ctx
        self.admin = admin
        super().__init__(data, per_page=8)

    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page
        embed = Embed(title="Player Menu 🤖", color=0xf1c40f)
        if self.admin and menu.current_page == 1:
            embed.title = "Admin Menu 🤖"

        for entry in entries:
            embed.add_field(name=entry["name"], value=entry["value"], inline=False)
        
        return embed

class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="help", description="Shows list of commands", with_app_command=True)
    @commands.check(in_animal_shop)
    async def help(self, ctx):
        data = [
            {"name": "!link [steam_id]", "value": "Link your Steam account to your Discord account."},
            {"name": "!pay", "value": "Give coins to other players."},
            {"name": "!coins", "value": "See your coins."},
            {"name": "!shop", "value": "Display the available animals for purchase."},
            {"name": "!buy [animal] [gender]", "value": "Buy an animal from the shop."},
            {"name": "!inject [animal] [slot]", "value": "Inject an animal into the game using a specified slot."},
            {"name": "!cage", "value": "Display your current balance and owned animals."},
        ]

        admin_role_id = 1183103584330588180
        if discord.utils.get(ctx.author.roles, id=admin_role_id) is not None:
            admin_data = [
                {"name": "!player", "value": "See your/other player info."},
                {"name": "!addcoins [user] [amount]", "value": "Add coins to a user's balance."},
                {"name": "!removecoins [user] [amount]", "value": "Remove coins from a user's balance."},
                {"name": "!addadmin [user]", "value": "Give admin privileges to a user in-game."},
                {"name": "!removeadmin [user]", "value": "Remove admin privileges from a user in-game."},
                {"name": "!clearcage [user]", "value": "Clear a player's cage."},
                {"name": "!strike [user] [reason]", "value": "Give a strike to a player (2 strikes results in a ban)."},
                {"name": "!warn [user] [reason]", "value": "Give a warning to a player (2 warnings result in a strike)."},
            ]
            
            data.extend(admin_data)
        
        pages = menus.MenuPages(source=HelpMenu(ctx, data, admin=True), clear_reactions_after=True)
        await pages.start(ctx)

async def setup(bot):
    await bot.add_cog(help(bot))