import discord
from discord.ext import commands

from .saveload import save_stats, load_stats


class UserStats(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.user_stats = load_stats()

    @commands.command(aliases=["reg"])
    async def register(self, ctx):
        user_id = str(ctx.author.id)
        stats = self.user_stats.get(user_id)

        if stats:
            await ctx.send("You have already registered! Use `stats` to check your profile.")
            return

        self.user_stats[user_id] = {
            "name": ctx.author.name,
            "level": 1,
            "coins": 100,
            "HP": 100,
            "ATK": 10,
            "DEF": 10, #10% of enemy's attack will be ignored
            "FAME": 1, #Maximum fame is 100 with high honor; minimum is -100 with low honor
            "SP": 10,
            "MP": 10
        }
        save_stats(self.user_stats)
        await ctx.send(f"✅ Registered {ctx.author.name} with default stats.")

    @commands.command(aliases=["stats"])
    async def statistics(self, ctx):
        user_id = str(ctx.author.id)
        stats = self.user_stats.get(user_id)

        if not stats:
            await ctx.send("❌ No stats found for you. Try registering first using `register`.")
            return

        chardata = {
            "Name": stats["name"],
            "Level": stats["level"],
            "Coins": f'¢{stats["coins"]}',
            "HP": stats["HP"],
            "ATK": stats["ATK"],
            "DEF": stats["DEF"],
            "FAME": stats["FAME"],
            "SP": stats["SP"],
            "MP": stats["MP"]
        }

        embed = discord.Embed(title="📊 Character Profile", color=discord.Colour.orange())
        embed.set_thumbnail(url=ctx.author.avatar.url)

        for label, value in chardata.items():
            embed.add_field(name=label, value=value, inline=True)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(UserStats(bot))