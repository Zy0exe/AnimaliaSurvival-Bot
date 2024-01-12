from functions import *
from import_lib import *

class QuestionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.question_channel_id = int(os.getenv("QUESTIONS_ID"))

    @commands.hybrid_command(name="question", description="Submit a question.", with_app_command=True)
    async def submit_questions(self, ctx, *, question: str):
        question_channel = self.bot.get_channel(self.question_channel_id)

        if question_channel is None:
            return await ctx.send("Question channel not found. Please contact the bot owner.")

        embed = discord.Embed(
            title="New Player Question ❓",
            description=question,
            color=0x3498DB,
        )
        embed.set_footer(text="Question Submitted")
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)

        await question_channel.send(embed=embed)

        acknowledgment_embed = discord.Embed(
            title="Question Sent ✅",
            description="Your question has been submitted!",
            color=discord.Color.green()
        )
        acknowledgment_msg = await ctx.send(embed=acknowledgment_embed, ephemeral=True)
        await asyncio.sleep(1)
        await acknowledgment_msg.delete()

async def setup(bot):
    await bot.add_cog(QuestionCog(bot))
