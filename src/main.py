import discord
from discord.ext import commands
from datetime import datetime, timezone, timedelta
import os

from dotenv import load_dotenv
load_dotenv()  # loads .env file into environment
TOKEN = os.getenv("TOKEN")

from .text_source.text_func import get_text

#-----------------------------------------------------------

BOT_CHANNEL_ID = 1360930885783912468
MASTER_ROLE_ID = 1435301288358449315

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="=", intents=intents)
bot.start_time = datetime.now(timezone.utc)

#-----------------------------------------------------------

#Import commands from commands.Bot files

from .status import change_status

bot.remove_command("help")

from .mod import silence, unsilence, smite, banish, banishid, unbanish, burn, EXPLOOOSION
for cmd in [silence, unsilence, smite, banish, banishid, unbanish, burn, EXPLOOOSION]:
    bot.add_command(cmd)

from .misc import placeholder, hello, parrot, mic, coin, dice, randnum
for cmd in [placeholder, hello, parrot, mic, coin, dice, randnum]:
    bot.add_command(cmd)

from .utility.utility import note, mynote, editnote, delnote, weather, language
for cmd in [note, mynote, editnote, delnote, weather, language]:
    bot.add_command(cmd)

from .sirius import orcus, orcustime, orcuscalc
for cmd in [orcus, orcustime, orcuscalc]:
    bot.add_command(cmd)

from .japanese.kotoba import entry, update, dictionary, vocabquiz, wordcount
for cmd in [entry, update, dictionary, vocabquiz, wordcount]:
    bot.add_command(cmd)

from .character.design import design
for cmd in [design]:
    bot.add_command(cmd)

from .character.element import designelements
for cmd in [designelements]:
    bot.add_command(cmd)

#-----------------------------------------------------------

RED = "\033[31m"
PURPLE = "\033[0;35m"
GREEN = "\033[32m"
GREY = "\033[90m"
BOLD = "\033[1m"
RESET = "\033[0m"

timenow = datetime.now(timezone(timedelta(hours=8))).replace(microsecond=0, tzinfo=None)

@bot.event
async def on_ready():        
    print(f"{PURPLE}{bot.user} {GREEN}has logged in! {BOLD}{GREY}{timenow}{RESET}")

    if not change_status.is_running():
        change_status.start(bot)

    #Import commands from commands.Cog files
    for ext in ["src.games.roulette", "src.rpgdata.userprofile", "src.masteronly", "src.info", "src.help"]:
        await bot.load_extension(ext)

@bot.event
async def on_disconnect():
    print(f'{PURPLE}{bot.user} {RED}has logged out. {BOLD}{GREY}{timenow}{RESET}')

@bot.event
async def on_resumed():
    print(f"{PURPLE}{bot.user} {GREEN}has resumed! {BOLD}{GREY}{timenow}{RESET}")

#-----------------------------------------------------------

#catch missing roles / permissions errors
@bot.event
async def on_command_error(ctx, error):
    text = get_text(ctx)["MAIN"]["on_command_error"]

    if isinstance(error, commands.MissingRole) and error.missing_role == MASTER_ROLE_ID:
        await ctx.send(text['not_master'])
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(text['lack_permission'])
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send(text['command_not_exist'])
    else:
        raise error

if __name__ == "__main__":
    bot.run(TOKEN)
