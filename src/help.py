import discord
from discord.ext import commands
from discord.ui import View, Select

from .text_source.text_func import get_text, get_text0

#------------------------------------------------------------------------------------

# HELP EMBEDS

def info_embed(ctx):
    info_text = get_text0(ctx)['HELP']['embeds']['info']
    info = discord.Embed(title=info_text['title'], description=info_text['desc'], color=discord.Color(0x90d5ff))            

    for key in ["aboutme", "serverinfo", "aboutuser", "avatar"]:
        info.add_field(
            name=info_text["fields"][key],
            value=info_text["values"][key],
            inline=False
        )

    return info

#---------------------------------------------

def mod_embed(ctx):
    mod_text = get_text0(ctx)['HELP']['embeds']['mod']
    mod = discord.Embed(title=mod_text['title'], description=mod_text['desc'], color=discord.Color(0xff0000))
    mod.set_footer(text=mod_text['footer'])

    for key in ["silence", "unsilence", "smite", "banish", "banishid", "unbanish", "burn", "EXPLOOOSION"]:
        mod.add_field(
            name=mod_text["fields"][key],
            value=mod_text["values"][key],
            inline=False
        )

    return mod

#---------------------------------------------

def game_embed(ctx):
    game_text = get_text0(ctx)['HELP']['embeds']['game']
    game = discord.Embed(title=game_text['title'], description=game_text['desc'], color=discord.Color(0xffffff))

    for key in ["roulette", "rpg"]:
        game.add_field(
            name=game_text["fields"][key],
            value=game_text["values"][key],
            inline=False
        )

    return game

#---------------------------------------------

def misc_embed(ctx):
    misc_text = get_text0(ctx)['HELP']['embeds']['misc']
    misc = discord.Embed(title=misc_text['title'], description=misc_text['desc'], color=discord.Color(0x000000))

    for key in ["placeholder", "hello", "parrot", "mic", "coin", "dice", "randnum"]:
        misc.add_field(
            name=misc_text["fields"][key],
            value=misc_text["values"][key],
            inline=False
        )

    return misc

#---------------------------------------------

def util_embed(ctx):
    util_text = get_text0(ctx)['HELP']['embeds']['util']
    utilities = discord.Embed(title=util_text['title'], description=util_text['desc'], color=discord.Color(0x4c3228))

    for key in ["note", "mynote", "editnote", "delnote", "weather", "language"]:
        utilities.add_field(
            name=util_text["fields"][key],
            value=util_text["values"][key],
            inline=False
        )
    
    return utilities

#---------------------------------------------

def profile_embed(ctx):
    profile_text = get_text0(ctx)['HELP']['embeds']['profile']
    profile = discord.Embed(title=profile_text['title'], description=profile_text['desc'], color=discord.Color.orange())

    for key in ["statistics", "register"]:
        profile.add_field(
            name=profile_text["fields"][key],
            value=profile_text["values"][key],
            inline=False
        )

    return profile

#---------------------------------------------

def sirius_embed(ctx):
    sirius_text = get_text0(ctx)['HELP']['embeds']['sirius']
    siriusa = discord.Embed(title=sirius_text['title'], description=sirius_text['desc'], color=discord.Color(0xf4abba))

    for key in ["orcus", "orcustime", "orcuscalc", "earthcalc"]:
        siriusa.add_field(
            name=sirius_text["fields"][key],
            value=sirius_text["values"][key],
            inline=False
        )

    return siriusa

#---------------------------------------------

def jp_embed(ctx):
    jp_text = get_text0(ctx)['HELP']['embeds']['jp']
    jp = discord.Embed(title=jp_text['title'], description=jp_text['desc'], color=discord.Color.purple())
    jp.set_footer(text=jp_text['footer'])

    for key in ["entry", "update", "list", "dictionary", "vocabquiz", "wordquiz", "kanjiquiz"]:
        jp.add_field(
            name=jp_text["fields"][key],
            value=jp_text["values"][key],
            inline=False
        )

    return jp

#---------------------------------------------

def design_embed(ctx):
    design_text = get_text0(ctx)['HELP']['embeds']['design']
    design = discord.Embed(title=design_text['title'], description=design_text['desc'], color=discord.Color.light_gray())
    design.set_footer(text=design_text['footer'])

    for key in ["design", "regendesign", "redesign", "alterdesign", "savedesign", "designlist"]:
        design.add_field(
            name=design_text["fields"][key],
            value=design_text["values"][key],
            inline=False
        )

    return design

#---------------------------------------------

def master_embed(ctx):
    master_text = get_text0(ctx)['HELP']['embeds']['master']
    master = discord.Embed(title=master_text['title'], description=master_text['desc'], color=discord.Color.dark_green())
    master.set_footer(text=master_text['footer'])

    for key in ["timerrun", "timercheck", "timerstop", "timerreset", "shutdown", "embedtest", "runtime", "mode", "modecheck"]:
        master.add_field(
            name=master_text["fields"][key],
            value=master_text["values"][key],
            inline=False
        )

    return master

#---------------------------------------------

def help1_embed(ctx):
    help1_text = get_text0(ctx)['HELP']['embeds']['help1']
    help1 = discord.Embed(description=help1_text['desc'], color=discord.Color.blurple())
    help1.set_author(name=help1_text['author'])
    help1.set_footer(text=help1_text['footer'])

    categories = get_text0(ctx)['HELP']['categories']

    for category, value in categories.items():
        help1.add_field(name=category, value=value, inline=False)

    return help1

#---------------------------------------------

def help2_embed(ctx):
    help2_text = get_text0(ctx)['HELP']['embeds']['help2']
    help2 = discord.Embed(description=help2_text['desc'], color=discord.Color.blurple())
    help2.set_author(name=help2_text['author'])
    help2.set_footer(text=help2_text['footer'])

    aliases = get_text0(ctx)['HELP']['aliases']

    for category, value in aliases.items():
            help2.add_field(name=category, value=value, inline=False)

    return help2

#------------------------------------------------------------------------------------

class HelpCategoryView(View):
    def __init__(self, author_id, ctx):
        super().__init__()

        self.author_id = author_id
        self.add_item(HelpCategorySelect(author_id, ctx))

class HelpCategorySelect(Select):
    def __init__(self, author_id, ctx):
        self.author_id = author_id
        self.ctx = ctx
        selections = get_text0(self.ctx)['HELP']['selections'] #selections is a list of category labels

        options = [discord.SelectOption(label=option) for option in selections]
        super().__init__(placeholder="Select a category", options=options)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("Only the command sender can use this menu.", ephemeral=True)
            return

        value = self.values[0]
        if value == "🩵 Information":
            embed = info_embed(self.ctx)

        elif value == "❤️ Moderation":
            embed = mod_embed(self.ctx)

        elif value == "🤍 Minigames":
            embed = game_embed(self.ctx)

        elif value == "🖤 Miscellaneous":
            embed = misc_embed(self.ctx)

        elif value == "🤎 Utilities":
            embed = util_embed(self.ctx)

        elif value == "🧡 Game Profile":
            embed = profile_embed(self.ctx)

        elif value == "🩷 Sirius Program":
            embed = sirius_embed(self.ctx)

        elif value == "💜 Japanese":
            embed = jp_embed(self.ctx)

        elif value == "🩶 Character Designer":
            embed = design_embed(self.ctx)

        elif value == "💚 Master Only":
            embed = master_embed(self.ctx)

        elif value == "Back to Help":
            embed = help1_embed(self.ctx)
        
        elif value == "Back to Help: Alias":
            embed = help2_embed(self.ctx)

        await interaction.response.edit_message(embed=embed, view=self.view)

#---------------------------------------------------------

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        help_text = get_text(ctx)["HELP"]["help_text"]

        embed = help1_embed(ctx)

        view = HelpCategoryView(ctx.author.id, ctx)
        await ctx.send(help_text, embed=embed, view=view)

    @commands.command()
    async def alhelp(self, ctx):
        help_text = get_text(ctx)["HELP"]["help_text"]

        embed = help2_embed(ctx)

        view = HelpCategoryView(ctx.author.id, ctx)
        await ctx.send(help_text, embed=embed, view=view)

    #---------------------------------------------------------

    @commands.command()
    async def information(self, ctx):
        embed = info_embed(ctx)
        await ctx.send(embed=embed)

    @commands.command()
    async def moderation(self, ctx):
        embed = mod_embed(ctx)
        await ctx.send(embed=embed)

    @commands.command()
    async def minigames(self, ctx):
        embed = game_embed(ctx)
        await ctx.send(embed=embed)

    @commands.command()
    async def miscellaneous(self, ctx):
        embed = misc_embed(ctx)
        await ctx.send(embed=embed)

    @commands.command()
    async def utility(self, ctx):
        embed = util_embed(ctx)
        await ctx.send(embed=embed)

    @commands.command()
    async def profile(self, ctx):
        embed = profile_embed(ctx)
        await ctx.send(embed=embed)

    @commands.command()
    async def sirius(self, ctx):
        embed = sirius_embed(ctx)
        await ctx.send(embed=embed)

    @commands.command()
    async def japanese(self, ctx):
        embed = jp_embed(ctx)
        await ctx.send(embed=embed)

    @commands.command()
    async def designer(self, ctx):
        embed = design_embed(ctx)
        await ctx.send(embed=embed)

    @commands.command()
    async def masteronly(self, ctx):
        embed = master_embed(ctx)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))