import discord
from discord.ext import commands
import asyncio

from ..background.design_calc import gender_pick, colors, outfit, accessory, hair, bangs, textile
from ..text_source.text_func import get_text0

import os
import json

#session path
folder = "character"
filename = "session.json"
path = os.path.join("src", folder, filename)

# Load database
def load_sesh_db():
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Write updated data to database
def write_sesh_db(session_data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(session_data, f, indent=4, ensure_ascii=False)

#Calculate randomizer, while also update the session file
def parse_session(w, weightless):
    sesh_db = load_sesh_db

    col = colors(w) if weightless == "true" else colors()
    fit = outfit()
    acc = accessory()
    hairs = hair(w) if weightless == "true" else hair()
    bang = bangs()
    tex = textile()

    #assign each key in db
    c = dict(zip(['ec', 'ecm', 's', 'hc', 'hcm', 'oc'], col))
    f = dict(zip(['hw', 'tw', 'aw', 'bw', 'fw'], fit))
    a = dict(zip(['ah', 'ag', 'at', 'aa', 'ab', 'af'], acc))
    h = dict(zip(['hl', 'hsm', 'hs', 'hct'], hairs))
    b = dict(zip(['bl', 'bp', 'bs'], bang))
    t = dict(zip(['p', 'pr', 'ex'], tex))

    col = ('bla', 'babdabd', 'aduhhab')
    new_sesh = {k: v for k, v in zip(['col', 'fit', 'acc', 'hair', 'bang', 'tex'], [c, f, a, h, b, t])}

    #write to db
    write_sesh_db(new_sesh)

    return col, fit, acc, hairs, bang, tex
        

#=========================================================================

@commands.command()
async def design(ctx, gender:str=None, weightless:str=None):
    text = get_text0(ctx)["DESIGNER"]["design"]
    text_err = text['errors']
    text_msg = text['messages']
    text_head = text['header']
    text_content = text['content']

    #-----------------------------------------------------------------------

    # DESIGN

    if isinstance(weightless, str):
        weightless = weightless.lower()

    if gender is None:
        embed = discord.Embed(
            title=text['title'],
            description=text['desc'],
            color=discord.Color.light_gray()
        )  
        embed.add_field(name=text['gender'], value=text['gen_args'], inline=False)
        embed.add_field(name=text['weightless'], value=text['weight_args'], inline=False)
        embed.add_field(name=text['notes'], value=text['notes_val'])
        await ctx.send(embed=embed)
        return

    if weightless in (None, "false"):
        pass
    elif weightless == "true":
        w = None
    else:
        embed = discord.Embed(
            title=text['title'],
            description=text['desc'],
            color=discord.Color.light_gray()
        )  
        embed.add_field(name=text['gender'], value=text['gen_args'], inline=False)
        embed.add_field(name=text['weightless'], value=text['weight_args'], inline=False)
        embed.add_field(name=text['notes'], value=text['notes_val'])
        
        await ctx.send(text_err['invalid_weightless'])
        await ctx.send(embed=embed)
        return
        
    chosen_gender = gender.lower()   
    valid_args = ['male', 'm', 'female', 'f', 'mix', 'random']

    if chosen_gender in valid_args:
        gender = gender_pick(chosen_gender)
    else:
        await ctx.send(text_err['invalid_gender'])
        return

    #get randomized attributes
    col, fit, acc, hairs, bang, tex = parse_session(w)

    ec, ecm, s, hc, hcm, oc = col
    hw, tw, aw, bw, fw = fit
    ah, ag, at, aa, ab, af = acc
    hl, hsm, hs, hct = hairs
    bl, bp, bs = bang
    p, pr, ex = tex

    ec, hc, oc = [", ".join(c) for c in [ec, hc, oc]]

    design_embed = discord.Embed(
        title=text_head['title'],
        description=text_head['desc'].format(gender=gender, weightless=weightless),
        color=discord.Color.light_gray()
    )
    design_embed.set_author(name=text_head['author'].format(ctx=ctx))

    design_embed.add_field(name=text_content['names']['color'], value=text_content['values']['color'].format(ec=ec,hc=hc,oc=oc))
    design_embed.add_field(name=text_content['names']['color_method'], value=text_content['values']['color_method1'].format(ecm=ecm,hcm=hcm) if not s else text_content['values']['color_method2'].format(ecm=ecm,s=s,hcm=hcm))
    design_embed.add_field(name=text_content['names']['hair'], value=text_content['values']['hair'].format(hl=hl,hsm=hsm,hs=hs,hct=hct))

    design_embed.add_field(name=text_content['names']['bangs'], value=text_content['values']['bangs'].format(bl=bl,bp=bp,bs=bs))
    design_embed.add_field(name=text_content['names']['outfit'], value=text_content['values']['outfit'].format(hw=hw,aw=aw,tw=tw,bw=bw,fw=fw))
    design_embed.add_field(name=text_content['names']['textile'], value=text_content['values']['textile'].format(p=p,pr=pr,ex=ex))

    design_embed.add_field(name=text_content['names']['accessory'], value=text_content['values']['accessory'].format(ah=ah,ag=ag,at=at,aa=aa,ab=ab,af=af))
    
    design_embed.set_footer(text=text_head['footer'])

    await ctx.send(embed=design_embed)

    #-----------------------------------------------------------------------
    # REDESIGN

    # check: only accept messages from the command invoker, in same channel
    def check(msg: discord.Message):
        return msg.author.id == ctx.author.id and msg.channel.id == ctx.channel.id

    while True:
        rtext = get_text0(ctx)["DESIGNER"]["redesign"]

        try:
            reply: discord.Message = await ctx.bot.wait_for("message", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            return

        embed = discord.Embed(
                title=rtext['title'],
                description=rtext['desc'],
                color=discord.Color.light_gray())  
        embed.add_field(
            name=rtext['arguments'], 
            value=rtext['args_val'],
            inline=False)
        embed.add_field(name=rtext['alias'], value="`=rdesign`")

        if reply.content in ["=redesign", "=rdesign", "=re"]:
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
                col, fit, acc, hairs, bang, tex = parse_session(w)

                ec, ecm, s, hc, hcm, oc = col
                hw, tw, aw, bw, fw = fit
                ah, ag, at, aa, ab, af = acc
                hl, hsm, hs, hct = hairs
                bl, bp, bs = bang
                p, pr, ex = tex

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
            return
    
'''@commands.command(aliases=["adesign"])
async def alterdesign(self, ctx, *, args:str=None):


@commands.command(aliases=["sdesign"])
async def savedesign(self, ctx, *, name:str=None):'''

