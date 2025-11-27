import discord
from discord.ext import commands, tasks
from random import choice

bot = commands.Bot(command_prefix="=", intents=discord.Intents.default())

activities = [
    discord.Game("Sirius Program"),
    discord.Game("Russian Roulette"),
    discord.Game("Tetris"),
    discord.Game("Minesweeper"),
    discord.Game("Atari Breakout"),
    discord.Game("Roblox"),

    discord.Activity(type=discord.ActivityType.watching, name="Master"),
    discord.Activity(type=discord.ActivityType.watching, name="Niche Animes that Master likes"),
    discord.Activity(type=discord.ActivityType.watching, name="Cooking Videos"),
    discord.Activity(type=discord.ActivityType.watching, name="Celestial Path of Sirius"),
    discord.Activity(type=discord.ActivityType.watching, name="The Night Sky"),

    discord.Activity(type=discord.ActivityType.listening, name="Master's Sleeping ASMR"),
    discord.Activity(type=discord.ActivityType.listening, name="Veronika's Russian Songs Playlist"),
    discord.Activity(type=discord.ActivityType.listening, name="Yorushika"),
    discord.Activity(type=discord.ActivityType.listening, name="ZUTOMAYO"),
    discord.Activity(type=discord.ActivityType.listening, name="Signal of Orcus"),
]

@tasks.loop(seconds=600)  # Change every 10 minutes
async def change_status(bot):
    activity = choice(activities)
    await bot.change_presence(activity=activity)