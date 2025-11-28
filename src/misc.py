import discord
from discord.ext import commands
from datetime import datetime, timezone
import random

from .text_source.text_func import get_text, get_text_neu

@commands.command(aliases=["ph"])
async def placeholder(ctx):
    text = get_text_neu(ctx)["MISC"]["placeholder"]

    embed = discord.Embed(
        title=text[0],
        description=text[1],
        color=discord.Color(0x000000),
        timestamp=datetime.now(timezone.utc),
    )
    embed.set_footer(text=text[2])
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/1431950377443528756/1431950572755488848/placeholder.png?ex=68ff4764&is=68fdf5e4&hm=6b8b0786453b51114131413ad542cb017732b8cb78f9c6dbaec259d2cc86ffe4&=&format=webp&quality=lossless&width=250&height=250")
    embed.set_image(url="https://media.discordapp.net/attachments/1431950377443528756/1431951120984707072/image.png?ex=68ff47e7&is=68fdf667&hm=1701ccc1b51f259287c848c38531d83eb9c58fe1c92dbebe2719b3cc6cd578ae&=&format=webp&quality=lossless&width=250&height=250")
    embed.set_author(name=text[3])
    embed.add_field(name=text[4], value=text[5], inline=True)
    embed.add_field(name=text[6], value=text[7], inline=True)
    
    await ctx.send(embed=embed)

@commands.command()
async def hello(ctx):
    text = get_text(ctx)["MISC"]["hello"]
    name = ctx.author.name
    await ctx.send(text.format(name=name))

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
    text = get_text(ctx)["MISC"]["coin"]
    side = random.choice([text[0], text[1]])
    await ctx.send(text[2].format(side=side))

@commands.command()
async def dice(ctx):
    await ctx.send(random.randint(1, 6))

@commands.command(aliases=["rand"])
async def randnum(ctx, num:int=100):
    await ctx.send(random.randint(1, num))