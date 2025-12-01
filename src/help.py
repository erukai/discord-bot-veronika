import discord
from discord.ext import commands
from discord.ui import View, Select

from .text_source.text_func import get_text

#---------------------------------------------------------

categories = {
    ":light_blue_heart: Information": "`aboutme` • `serverinfo` • `aboutuser` • `avatar`",
    ":heart: Moderation": "`silence` • `unsilence` • `smite` • `banish` • `banishid` • `unbanish` • `burn` • `EXPLOOOSION`",
    ":white_heart: Minigames": "`roulette` 🔄 • `rpg` ❌",
    ":black_heart: Miscellaneous": "`placeholder` • `hello` • `parrot` • `mic` • `coin` • `dice` • `randnum`",
    ":brown_heart: Utilities": "`note` • `mynote` • `editnote` • `delnote` • `weather` • `language`",
    ":orange_heart: Game Profile": "`stats` • `register`",
    ":pink_heart: Sirius Program": "`orcus` • `orcustime` • `orcuscalc` • `earthcalc` ❌",
    ":purple_heart: Japanese": "`entry` • `update` • `list` ❌ • `dictionary` • `vocabquiz` • `wordquiz` ❌ • `kanjiquiz` ❌",
    ":grey_heart: Character Designer": "`design` • `redesign` ❌ • `alterdesign` ❌ • `savedesign` ❌ • `designlist` ❌",
    ":green_heart: Master Only": "`timerrun` • `timerstop` • `timercheck` • `timerreset` • `shutdown` • `embedtest` • `runtime` • `mode` • `modecheck`",
    ":sparkles: Reactions": "`right?` • `i summon thee` • `you there` • `slave` • `sorry` • `good girl` • `good night` • `clanker`",
}

aliases = {
    ":light_blue_heart: Information": "`me` • `info` • `user` • `av`",
    ":heart: Moderation": "`mute` • `unmute` • `kick` • `ban` • `banid` • `unban` • `purge` • `nuke` / `ex`",
    ":white_heart: Minigames": "`gun` 🔄 • `game` ❌",
    ":black_heart: Miscellaneous": "`ph` • _`hello`_ • _`parrot`_ • _`mic`_ • _`coin`_ • _`dice`_ • `rand`",
    ":brown_heart: Utilities": "`n` • `mn` • `en` • `dn` • `wt` • `lang`",
    ":orange_heart: Game Profile": "_`stats`_ • `reg`",
    ":pink_heart: Sirius Program": "`or` • `ot` • `oc` • `ec` ❌",
    ":purple_heart: Japanese": "`kotoba` / `koto` • `up` • _`list`_ ❌ • `dict` • `vocab` / `vq` • `word` / `wq` ❌ • `kanji` / `kq` ❌",
    ":grey_heart: Character Designer": "_`design`_ • `rdesign` ❌ • `adesign` ❌ • `sdesign` ❌ • `mydesign` ❌",
    ":green_heart: Master Only": "`trun` • `ts` • `tc` • `tr` • `sd` • `et` • `rt` • `md` • `mc`",
    ":sparkles: Reactions:": "`correct?` • _`i summon thee`_ • _`you there`_ • _`slave`_ • `my bad` / `my fault` / `apologize` • _`good girl`_ • _`good night`_ • `clanka`",
}

#------------------------------------------------------------------------------------

# HELP EMBEDS

info = discord.Embed(title=":light_blue_heart: Information", description="Information about this server and its members.", color=discord.Color(0x90d5ff))            

info.add_field(name="`aboutme` _(alias: `me`)_", value="Introduction to the bot.\n`< =aboutme >`", inline=False)
info.add_field(name="`serverinfo` _(alias: `info`)_", value="Get information about the server.\n`< =serverinfo >`", inline=False)
info.add_field(name="`aboutuser` _(alias: `user`)_", value="Get information about a user.\n`< =aboutuser >`", inline=False)
info.add_field(name="`avatar` _(alias: `av`)_", value="Get a user's avatar.\n`< =avatar >`", inline=False)

#---------------------------------------------

mod = discord.Embed(title=":heart: Moderation", description="Moderation tools for this server.", color=discord.Color(0xff0000))

mod.add_field(name="`silence` _(alias: `mute`)_", value="Mute a user within a set duration.\n`< =silence [@user] [duration: s, m, h, d] [reason (opt.)] >`", inline=False)
mod.add_field(name="`unsilence` _(alias: `unmute`)_", value="Unmute a muted user.\n`< =unsilence [@user] >`", inline=False)
mod.add_field(name="`smite` _(alias: `kick`)_", value="Kick a user.\n`< =smite [@user] [reason (opt.)] >`", inline=False)
mod.add_field(name="`banish` _(alias: `ban`)_", value="Ban a user.\n`< =banish [@user] [reason (opt.)] >`", inline=False)
mod.add_field(name="`banishid` _(alias: `banid`)_", value="Ban a user by ID.\n`< =banish [user_id: int] [reason (opt.)] >`", inline=False)
mod.add_field(name="`unbanish` _(alias: `unban`)_", value="Unban a banned user.\n`< =unbanish [user_id: int] >`", inline=False)
mod.add_field(name="`burn` _(alias: `purge`)_", value="Delete past messages in a channel.\n`< =burn [amount: <= 100] >`", inline=False)
mod.add_field(name="`EXPLOOOSION` _(alias: `nuke`, `ex`)_", value="Delete ALL messages in a channel.\n`< =EXPLOOOSION >`", inline=False)

mod.set_footer(text="'opt.' stands for 'optional'.")

#---------------------------------------------

game = discord.Embed(title=":white_heart: Minigames", description="Minigames to play with others or alone.", color=discord.Color(0xffffff))

game.add_field(name="`roulette` _(alias: `gun`)_", value="Start a round of Russian Roulette with the bot or another player.\n`< =roulette >`", inline=False)
game.add_field(name="`rpg` :x: _(alias: `game`)_", value="Start or continue your RPG adventure.\n`< =rpg >`", inline=False)

#---------------------------------------------

misc = discord.Embed(title=":black_heart: Miscellaneous", description="Random commands to use.", color=discord.Color(0x000000))

misc.add_field(name="`placeholder` _(alias: `ph`)_", value="Get a placeholder embed.\n`< =placeholder >`", inline=False)
misc.add_field(name="`hello`", value="Greet the bot.\n`< =hello >`", inline=False)
misc.add_field(name="`parrot`", value="Make the bot repeat your message.\n`< =parrot >`", inline=False)
misc.add_field(name="`mic`", value="Make the bot repeat your message and delete the command.\n`< =mic >`", inline=False)
misc.add_field(name="`coin`", value="Flip a coin.\n`< =coin >`", inline=False)
misc.add_field(name="`dice`", value="Get a random number between 1 and 6.\n`< =dice >`", inline=False)
misc.add_field(name="`randnum` _(alias: `rand`)_", value="Get a random number between 1 and a number of your choice (`default=100`).\n`< =randnum [amount] >`", inline=False)

#---------------------------------------------

utilities = discord.Embed(title=":brown_heart: Utilities", description="Useful general tools.", color=discord.Color(0x4c3228))

utilities.add_field(name="`note` _(alias: `n`)_", value="Add a note to your profile.\n`< =note [text] >`", inline=False)
utilities.add_field(name="`mynote` _(alias: `mn`)_", value="View your notes.\n`< =mynote >`", inline=False)
utilities.add_field(name="`editnote` _(alias: `en`)_", value="Edit a note by index.\n`< =editnote [index] [text] >`", inline=False)
utilities.add_field(name="`delnote` _(alias: `dn`)_", value="Delete a note by index.\n`< =delnote [index] >`", inline=False)
utilities.add_field(name="`weather` _(alias: `wt`)_", value="Get the current weather of a city.\n`< =weather [measurement] [city] >`", inline=False)
utilities.add_field(name="`language` _(alias: `lang`)_", value="Change the bot's language (user-specific).\n`< =language [code] >`", inline=False)

#---------------------------------------------

profile = discord.Embed(title=":orange_heart: Game Profile", description="Your character profile to play minigames.", color=discord.Color.orange())

profile.add_field(name="`statistics` _(alias: `stats`)_", value="Check your character's statistics.\n`< =statistics >`", inline=False)
profile.add_field(name="`register` _(alias: `reg`)_", value="Register your character profile.\n`< =register >`", inline=False)

#---------------------------------------------

siriusa = discord.Embed(title=":pink_heart: Sirius Program", description="Information or calculations of the Sirius world.", color=discord.Color(0xf4abba))
            
siriusa.add_field(name="`orcus` _(alias: `or`)_", value="Get the current time on Orcus and delete the command.\n`< =orcus >`", inline=False)
siriusa.add_field(name="`orcustime` _(alias: `ot`)_", value="Get the current time on Orcus.\n`< =orcustime >`", inline=False)
siriusa.add_field(name="`orcuscalc` _(alias: `oc`)_", value="Get the time on Orcus aligned to the set Earth date.\n`< =orcuscalc [day: <= 28~31] [month: <= 12] [year: >= 10 CE] >`\n_separators:_ ` ` `,` `;` `+` `|`", inline=False)
siriusa.add_field(name="`earthcalc` :x: _(alias: `ec`)_", value="Get the time on Earth aligned to the set Orcus date.\n`< =earthcalc [day: <= 50 or 61~62] [month: <= 30] [year: >= 3235 SY] >`\n_separators:_ ` ` `,` `;` `+` `|`", inline=False)

#---------------------------------------------

jp = discord.Embed(title=":purple_heart: Japanese", description="Tools for Master's Japanese language study. Do not touch if you're not Master.", color=discord.Color.purple())
            
jp.add_field(name="`entry` _(alias: `kotoba`, `koto`)_", value="Store a Japanese word into the database (must contain kanji).\n`< =kotoba [word]; [romaji]; [part of speech]; [word meaning]; [kanji meaning]; [note (opt.)] >`\n_separators:_ `_` `;` `+` `|` `[new line]`", inline=False)
jp.add_field(name="`update` _(alias: `up`)_", value="Update a data of a stored word.\n`< =update w:[word] p:[romaji] r:[role] m:[meaning] km:[kanji meaning] >`\n_prefixes:_ `w:` `p:` `r:` `m:` `km:`", inline=False)
jp.add_field(name="`list` :x:", value="Get a list of stored words with set filters.\n`< =list ~~~ >`", inline=False)
jp.add_field(name="`dictionary` _(alias: `dict`)_", value="Get the data of a word from the database.\n`< =dictionary [word] >`", inline=False)
jp.add_field(name="`vocabquiz` _(alias: `vocab`, `vq`)_", value="Start a session of vocabulary quiz.\n`< =vocabquiz [rounds (opt.)] [roles (opt.)] [kanji count (opt.)] >`\n_separators:_ ` ` `,` `;` | roles separator: `.`", inline=False)
jp.add_field(name="`wordquiz` :x: _(alias: `word`, `wq`)_", value="Start a session of word quiz.\n`< =wordquiz ~~~ >`", inline=False)
jp.add_field(name="`kanjiquiz` :x: _(alias: `kanji`, `kq`)_", value="Start a session of kanji quiz.\n`< =kanjiquiz ~~~ >`", inline=False)

jp.set_footer(text="'opt.' stands for 'optional'.")

#---------------------------------------------

char = discord.Embed(title=":grey_heart: Character Designer", description="Character design generator.", color=discord.Color.light_gray())

char.add_field(name="`design`", value="Generate a random character design.\n`< =design [gender: m, f, mix, random] [weightless (optional): bool] >`", inline=False)
char.add_field(name="`regendesign` _(alias: `rgdesign`)_", value="Regenerate a new character design using the previous arguments.\n`< =regendesign >`", inline=False)
char.add_field(name="`redesign` _(alias: `rdesign`)_", value="Regenerate an element of the generated design.\n`< =redesign prefix:[element] >`", inline=False)
char.add_field(name="`alterdesign` _(alias: `adesign`)_", value="Manually alter an element of the generated design.\n`< =alterdesign prefix:[element] >`", inline=False)
char.add_field(name="`savedesign` _(alias: `sdesign`)_", value="Save a generated design.\n`< =savedesign [design_name] >`", inline=False)
char.add_field(name="`designlist` _(alias: `mydesign`)_", value="Get a list of saved designs.\n`< =designlist >`", inline=False)

char.set_footer(text="Get the full list of elements in Character Designer and their prefixes with `=designelements` (alias: `=edesign`)")

#---------------------------------------------

master = discord.Embed(title=":green_heart: Master Only", description="Tools and commands that are exclusive to Master.", color=discord.Color.dark_green())
        
master.add_field(name="`timerrun` _(alias: `trun`)_", value="Start a timer that loops every 14 minutes.\nThis command sends a reminder at the end of each loop.\n`< =timerrun >`", inline=False)
master.add_field(name="`timercheck` _(alias: `tc`)_", value="Check the remaining time (in minutes) before the next loop.\n`< =timercheck >`", inline=False)
master.add_field(name="`timerstop` _(alias: `ts`)_", value="Stop the running timer loop.\n`< =timerstop >`", inline=False)
master.add_field(name="`timerreset` _(alias: `tr`)_", value="Reset the timer loop.\n`< =timerreset >`", inline=False)
master.add_field(name="`shutdown` _(alias: `sd`)_", value="Shut the bot down. **[RESTRICTED BY MASTER ID]**\n`< =shutdown >`", inline=False)
master.add_field(name="`embedtest` _(alias: `et`)_", value="For embed testing.\n`< =embedtest >`", inline=False)
master.add_field(name="`runtime` _(alias: `rt`)_", value="Check the bot's run time since startup.\n`< =runtime >`", inline=False)
master.add_field(name="`mode` _(alias: `md`)_", value="Switch between normal mode and master mode (determines Veronika's way of talking to Master)\n`< =mode [mode (opt.)] >`", inline=False)
master.add_field(name="`modecheck` _(alias: `mc`)_", value="Check current mode between Master and Veronika.\n`< =modecheck >`", inline=False)

master.set_footer(text="'opt.' stands for 'optional'.")

#---------------------------------------------

help1 = discord.Embed(description='_◈ Prefix: "="_', color=discord.Color.blurple())
help1.set_author(name="Commands List")
help1.set_footer(text="Use =alhelp for command aliases")

for category, value in categories.items():
    help1.add_field(name=category, value=value, inline=False)

#---------------------------------------------

help2 = discord.Embed(description='_◈ Prefix: "="_', color=discord.Color.blurple())
help2.set_author(name="Commands List: Aliases")
help2.set_footer(text="Use =help for full commands")

for category, value in aliases.items():
        help2.add_field(name=category, value=value, inline=False)

#------------------------------------------------------------------------------------

class HelpCategoryView(View):
    def __init__(self, author_id):
        super().__init__()
        self.author_id = author_id
        self.add_item(HelpCategorySelect(self.author_id))

class HelpCategorySelect(Select):
    def __init__(self, author_id):
        self.author_id = author_id
        options = [
            discord.SelectOption(label=option) for option in [
                "🩵 Information", "❤️ Moderation", "🤍 Minigames", "🖤 Miscellaneous", "🤎 Utilities", "🧡 Game Profile",
                "🩷 Sirius Program", "💜 Japanese", "🩶 Character Designer", "💚 Master Only", "Back to Help", "Back to Help: Alias"
            ]
        ]
        super().__init__(placeholder="Select a category", options=options)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("Only the command sender can use this menu.", ephemeral=True)
            return

        value = self.values[0]
        if value == "🩵 Information":
            embed = info

        elif value == "❤️ Moderation":
            embed = mod

        elif value == "🤍 Minigames":
            embed = game

        elif value == "🖤 Miscellaneous":
            embed = misc

        elif value == "🤎 Utilities":
            embed = utilities

        elif value == "🧡 Game Profile":
            embed = profile

        elif value == "🩷 Sirius Program":
            embed = siriusa

        elif value == "💜 Japanese":
            embed = jp

        elif value == "🩶 Character Designer":
            embed = char

        elif value == "💚 Master Only":
            embed = master

        elif value == "Back to Help":
            embed = help1
        
        elif value == "Back to Help: Alias":
            embed = help2

        await interaction.response.edit_message(embed=embed, view=self.view)

#---------------------------------------------------------

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        help_text = get_text(ctx)["HELP"]["help_text"]

        embed = help1

        view = HelpCategoryView(ctx.author.id)
        await ctx.send(help_text, embed=embed, view=view)

    @commands.command()
    async def alhelp(self, ctx):
        help_text = get_text(ctx)["HELP"]["help_text"]

        embed = help2

        view = HelpCategoryView(ctx.author.id)
        await ctx.send(help_text, embed=embed, view=view)

    #---------------------------------------------------------

    @commands.command()
    async def information(self, ctx):
        embed = info
        await ctx.send(embed=embed)

    @commands.command()
    async def moderation(self, ctx):
        embed = mod
        await ctx.send(embed=embed)

    @commands.command()
    async def minigames(self, ctx):
        embed = game
        await ctx.send(embed=embed)

    @commands.command()
    async def miscellaneous(self, ctx):
        embed = misc
        await ctx.send(embed=embed)

    @commands.command()
    async def utility(self, ctx):
        embed = utilities
        await ctx.send(embed=embed)

    @commands.command()
    async def gameprofile(self, ctx):
        embed = profile
        await ctx.send(embed=embed)

    @commands.command()
    async def sirius(self, ctx):
        embed = siriusa
        await ctx.send(embed=embed)

    @commands.command()
    async def japanese(self, ctx):
        embed = jp
        await ctx.send(embed=embed)

    @commands.command()
    async def designer(self, ctx):
        embed = char
        await ctx.send(embed=embed)

    @commands.command()
    async def masteronly(self, ctx):
        embed = master
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))