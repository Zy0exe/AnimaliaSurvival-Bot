from functions import *
from import_lib import *

class SuggestionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.suggestion_channel_id = int(os.getenv("SUGGESTION_ID"))

    @commands.hybrid_command(name="suggestion", aliases=["suggest"], description="Submit a suggestion.", with_app_command=True)
    async def submit_suggestion(self, ctx, *, suggestion: str):
        suggestion_channel = self.bot.get_channel(self.suggestion_channel_id)

        if suggestion_channel is None:
            return await ctx.send("Suggestion channel not found. Please contact the bot owner.")

        embed = discord.Embed(
            title="New Suggestion 🚀",
            description=suggestion,
            color=0x3498DB,
        )
        embed.set_footer(text="Suggestion Submited")
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)

        await suggestion_channel.send(embed=embed)

        acknowledgment_embed = discord.Embed(
            title="Suggestion Sent ✅",
            description="Your suggestion has been submitted!",
            color=discord.Color.green()
        )
        acknowledgment_msg = await ctx.send(embed=acknowledgment_embed, ephemeral=True)
        await asyncio.sleep(1)
        await acknowledgment_msg.delete()

async def setup(bot):
    await bot.add_cog(SuggestionCog(bot))