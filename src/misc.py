import discord
from discord.ext import commands
from datetime import datetime, timezone
import random

from .modeset.mode_func import get_text

@commands.command(aliases=["ph"])
async def placeholder(ctx):

    embed = discord.Embed(
        title="Title",
        description="This is is the description.",
        color=discord.Color(0x000000),
        timestamp=datetime.now(timezone.utc),
    )
    embed.set_footer(text="This is the footer.")
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/1431950377443528756/1431950572755488848/placeholder.png?ex=68ff4764&is=68fdf5e4&hm=6b8b0786453b51114131413ad542cb017732b8cb78f9c6dbaec259d2cc86ffe4&=&format=webp&quality=lossless&width=250&height=250")
    embed.set_image(url="https://media.discordapp.net/attachments/1431950377443528756/1431951120984707072/image.png?ex=68ff47e7&is=68fdf667&hm=1701ccc1b51f259287c848c38531d83eb9c58fe1c92dbebe2719b3cc6cd578ae&=&format=webp&quality=lossless&width=250&height=250")
    embed.set_author(name="Author Section")
    embed.add_field(name="Sub-title1", value="Sub-description1", inline=True)
    embed.add_field(name="Sub-title2", value="Sub-description2", inline=True)
    
    await ctx.send(embed=embed)

@commands.command()
async def hello(ctx):
    text_db = get_text(ctx)
    hello_text = text_db["MISC"]["hello"]

    await ctx.send(hello_text)

@commands.command()
async def parrot(ctx, *, message:str):
    await ctx.send(f"{message.capitalize()}")

@commands.command()
async def mic(ctx, *, msg:str):

    copy = msg
    async for msg in ctx.channel.history(limit=1):
        if msg.author == ctx.author:
            await msg.delete()
            break

    await ctx.send(f"{copy}")

@commands.command()
async def coin(ctx):
    side = ["heads", "tails"]
    await ctx.send(f"Coin flipped! You get {random.choice(side)}!")

@commands.command()
async def dice(ctx):
    await ctx.send(random.randint(1, 6))

@commands.command(aliases=["rand"])
async def randnum(ctx, num:int=100):
    await ctx.send(random.randint(1, num))