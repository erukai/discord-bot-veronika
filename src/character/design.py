import discord
from discord.ext import commands

from ..background.design_calc import gender_pick, colors, outfit, accessory, hair, bangs, textile

#=========================================================================

@commands.command()
async def design(ctx, gender:str=None, weightless:str=None):

    if isinstance(weightless, str):
        weightless = weightless.lower()

    if gender is None:
        embed = discord.Embed(
            title="Syntax:",
            description="`=design [gender] [weightless (opt.)]`",
            color=discord.Color.light_gray()
        )  
        embed.add_field(name="`[gender]` Arguments:", value="- `male` / `m`, `female` / `f`, `mix`, `random`", inline=False)
        embed.add_field(name="`[weightless]` Arguments:", value="- `True`, `False` (default = `False`)\n_(Case is not sensitive.)_", inline=False)
        embed.add_field(name="Notes", value="- `mix` = both male and female elements will be generated\n- `random` = either male or female elements will be generated")
        await ctx.send(embed=embed)
        return

    if weightless in (None, "false"):
        pass
    elif weightless == "true":
        w = None
    else:
        embed = discord.Embed(
            title="Syntax:",
            description="`=design [gender] [weightless (opt.)]`",
            color=discord.Color.light_gray()
        )  
        embed.add_field(name="`[gender]` Arguments:", value="- `male` / `m`, `female` / `f`, `mix`, `random`", inline=False)
        embed.add_field(name="`[weightless]` Arguments:", value="- `True`, `False` (default = `False`)\n_(Case is not sensitive.)_", inline=False)
        embed.add_field(name="Notes", value="- `mix` = both male and female elements will be generated\n- `random` = either male or female elements will be generated")
        
        await ctx.send("Argument `weightless` only accepts `true` or `false`!")
        await ctx.send(embed=embed)
        return
        
    chosen_gender = gender.lower()   
    valid_args = ['male', 'm', 'female', 'f', 'mix', 'random']

    if chosen_gender in valid_args:
        gender = gender_pick(chosen_gender)
    else:
        await ctx.send("The argument provided is not valid!")
        return

    #get randomized attributes
    ec, ecm, s, hc, hcm, oc = colors(w) if weightless == "true" else colors()
    hw, tw, aw, bw, fw = outfit()
    ah, ag, at, aa, ab, af = accessory()
    hl, hsm, hs, hct = hair(w) if weightless == "true" else hair()
    bl, bp, bs = bangs()
    p, pr, ex = textile()

    ec, hc, oc = [", ".join(c) for c in [ec, hc, oc]]

    design_embed = discord.Embed(
        title="Character Design",
        description=f"Gender: {gender.capitalize()}, Weightless: {weightless.capitalize() if isinstance(weightless, str) else weightless}",
        color=discord.Color.light_gray()
    )
    design_embed.set_author(name=f"{ctx.author.name}'s design")

    design_embed.add_field(name="COLORS", value=f"- eye color(s): {ec}\n- hair color(s): {hc}\n- outfit color(s): {oc}")
    design_embed.add_field(name="COLOR METHODS", value=f"- eye color method: {ecm}\n- hair color method: {hcm}" if not s else f"- eye color method: {ecm}\n- pupil shape: {s}\n- hair color method: {hcm}")
    design_embed.add_field(name="HAIR", value=f"- hair length: {hl}\n- hair symmetry: {hsm}\n- hair style: {hs}\n- haircut: {hct}")

    design_embed.add_field(name="BANGS", value=f"- bangs length: {bl}\n- bangs position: {bp}\n- bangs style: {bs}")
    design_embed.add_field(name="OUTFIT", value=f"- headwear: {hw}\n- topwear: {tw}\n- armwear: {aw}\n- bottomwear: {bw}\n- footwear: {fw}")
    design_embed.add_field(name="TEXTILE", value=f"- pattern: {p}\n- print: {pr}\n- exotic: {ex}")

    design_embed.add_field(name="ACCESSORIES", value=f"- hair ornament: {ah}\n- general: {ag}\n- top accessory: {at}\n- arm accessory: {aa}\n- bottom accessory: {ab}\n- foot accessory: {af}")
    
    design_embed.set_footer(text="Follow up commands: =redesign, =alterdesign, =savedesign")

    await ctx.send(embed=design_embed)



    '''# check: only accept messages from the command invoker, in same channel
    def check(msg: discord.Message):
        return msg.author.id == ctx.author.id and msg.channel.id == ctx.channel.id

    while True:
        try:
            reply: discord.Message = await ctx.bot.wait_for("message", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            return

        embed = discord.Embed(
                title="Syntax:",
                description="`=redesign [short attribute name]`",
                color=discord.Color.light_gray())  
        embed.add_field(
            name="Valid Arguments", 
            value="- color: `ec`, `ecm`, `s`, `hc`, `hcm`, `oc`\n- outfit: `hw`, `tw`, `aw`, `bw`, `fw`\n- accessory: `ah`, `ag`, `at`, `aa`, `ab`, `af`\n- hair: `hl`, `hsm`, `hs`, `hct`\n- bangs: `bl`, `bp`, `bs`\n- textile: `p`, `pr`, `ex`", 
            inline=False)
        embed.add_field(name="Alias", value="`=rdesign`")

        if reply.content in ["=redesign", "=rdesign"]:
            await ctx.send(embed=embed)
            return
        
        elif any(["=redesign", "=rdesign", "=re"]) in reply.content:
            attributes = {
                'col' : ['ec', 'ecm', 's', 'hc', 'hcm', 'oc'],
                'fit' : ['hw', 'tw', 'aw', 'bw', 'fw'],
                'acc' : ['ah', 'ag', 'at', 'aa', 'ab', 'af'],
                'hair' : ['hl', 'hsm', 'hs', 'hct'],
                'bang' : ['bl', 'bp', 'bs'],
                'textile' : ['p', 'pr', 'ex']
            }
            all_attr = [item for sublist in attributes.values() for item in sublist]

            copy = reply.content
            for keyword in ["=redesign", "=rdesign"]:
                copy = copy.replace(keyword, "")
            message = copy.strip().split()

            if any(w not in all_attr for w in message):
                ctx.send("Invalid argument! Insert only element shortcuts")
            else:
                

            #new randomized attributes
            ec2, ecm2, s2, hc2, hcm2, oc2 = colors()
            hw2, tw2, aw2, bw2, fw2 = outfit()
            ah, ag, at, aa, ab, af = accessory()
            hl, hsm, hs, hct = hair()
            bl, bp, bs = bangs()
            p, pr, ex = textile()

            ec, hc, oc = [", ".join(c) for c in [ec, hc, oc]]



        elif reply.content == "=alterdesign":
            break



        elif reply.content == "=savedesign":

            if gender is None:
                embed = discord.Embed(
                    title="Syntax:",
                    description="`=design [gender]`",
                    color=discord.Color.light_gray()
                )  
                embed.add_field(name="Valid Arguments", value="`male` / `m`, `female` / `f`, `mix`, `random`", inline=False)
                embed.add_field(name="Notes", value="- `mix` = both male and female elements will be generated\n- `random` = either male or female elements will be generated")
                await ctx.send(embed=embed)
                return


            break



        else:
            return'''
    
'''@commands.command(aliases=["adesign"])
async def alterdesign(self, ctx, *, args:str=None):


@commands.command(aliases=["sdesign"])
async def savedesign(self, ctx, *, name:str=None):'''
        



