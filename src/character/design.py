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
def parse_session(gender, w, weightless, user_id):
    sesh_db = load_sesh_db()

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

    sesh_db[user_id] = {
        k: v for k, v in zip(
            ['gender', 'weightless', 'col', 'fit', 'acc', 'hair', 'bang', 'tex'], [gender, weightless, c, f, a, h, b, t]
        )
    }

    #write to db
    write_sesh_db(sesh_db)

    return col, fit, acc, hairs, bang, tex
        

#=========================================================================

@commands.command()
async def design(ctx, gender:str=None, weightless:str=None):
    text = get_text0(ctx)["DESIGNER"]["design"]
    text_err = text['errors']
    text_msg = text['messages']
    text_head = text['header']
    text_content = text['content']

    user_id = str(ctx.author.id)

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

    w = None #IMPORTANT: although w is assigned, it will only be used as an argument in randomizer if weightless = True

    if isinstance(weightless, str):
        weightless = weightless.lower()

    if weightless not in (None, "false", "true"):        
        await ctx.send(text_err['invalid_weightless'])
        return
        
    chosen_gender = gender.lower()   
    valid_args = ['male', 'm', 'female', 'f', 'mix', 'random']

    if chosen_gender in valid_args:
        gender = gender_pick(chosen_gender)
    else:
        await ctx.send(text_err['invalid_gender'])
        return

    #get randomized attributes
    col, fit, acc, hairs, bang, tex = parse_session(gender, w, weightless, user_id)

    ec, ecm, s, hc, hcm, oc = col
    hw, tw, aw, bw, fw = fit
    ah, ag, at, aa, ab, af = acc
    hl, hsm, hs, hct = hairs
    bl, bp, bs = bang
    p, pr, ex = tex

    ec, hc, oc = [", ".join(c) for c in [ec, hc, oc]]

    design_embed = discord.Embed(
        title=text_head['title'],
        description=text_head['desc'].format(gender=gender.capitalize(),
            weightless=weightless.capitalize() if isinstance(weightless, str) else weightless),
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

    await ctx.send(text_msg['success'])
    await ctx.send(embed=design_embed)


@commands.command(aliases=["rgdesign", "regen"])
async def regendesign(ctx):
    text = get_text0(ctx)["DESIGNER"]["regendesign"]
    text_err = text['errors']
    text_msg = text['messages']

    embed_text = get_text0(ctx)["DESIGNER"]["design"]
    embed_head = embed_text['header']
    embed_content = embed_text['content']

    sesh_db = load_sesh_db()
    user_id = str(ctx.author.id)

    #if no sessions, send error
    try:
        user_sesh = sesh_db[user_id]
    except KeyError:
        await ctx.send(text_err['no_session'])
        return
    
    gender = user_sesh['gender']
    weightless = user_sesh['weightless']
    w = None #IMPORTANT: although w is assigned, it will only be used as an argument in randomizer if weightless = True
    
    #get randomized attributes
    col, fit, acc, hairs, bang, tex = parse_session(gender, w, weightless, user_id)

    ec, ecm, s, hc, hcm, oc = col
    hw, tw, aw, bw, fw = fit
    ah, ag, at, aa, ab, af = acc
    hl, hsm, hs, hct = hairs
    bl, bp, bs = bang
    p, pr, ex = tex

    ec, hc, oc = [", ".join(c) for c in [ec, hc, oc]]

    design_embed = discord.Embed(
        title=embed_head['title'],
        description=embed_head['desc'].format(gender=gender.capitalize(),
            weightless=weightless.capitalize() if isinstance(weightless, str) else weightless),
        color=discord.Color.light_gray()
    )
    design_embed.set_author(name=embed_head['author'].format(ctx=ctx))

    design_embed.add_field(name=embed_content['names']['color'], value=embed_content['values']['color'].format(ec=ec,hc=hc,oc=oc))
    design_embed.add_field(name=embed_content['names']['color_method'], value=embed_content['values']['color_method1'].format(ecm=ecm,hcm=hcm) if not s else embed_content['values']['color_method2'].format(ecm=ecm,s=s,hcm=hcm))
    design_embed.add_field(name=embed_content['names']['hair'], value=embed_content['values']['hair'].format(hl=hl,hsm=hsm,hs=hs,hct=hct))

    design_embed.add_field(name=embed_content['names']['bangs'], value=embed_content['values']['bangs'].format(bl=bl,bp=bp,bs=bs))
    design_embed.add_field(name=embed_content['names']['outfit'], value=embed_content['values']['outfit'].format(hw=hw,aw=aw,tw=tw,bw=bw,fw=fw))
    design_embed.add_field(name=embed_content['names']['textile'], value=embed_content['values']['textile'].format(p=p,pr=pr,ex=ex))

    design_embed.add_field(name=embed_content['names']['accessory'], value=embed_content['values']['accessory'].format(ah=ah,ag=ag,at=at,aa=aa,ab=ab,af=af))
    
    design_embed.set_footer(text=embed_head['footer'])

    await ctx.send(text_msg['success'])
    await ctx.send(embed=design_embed)



'''@commands.command(aliases=["rdesign", "re"])
async def redesign(ctx, *, args:str=None):


@commands.command(aliases=["adesign", "alt"])
async def alterdesign(ctx, *, args:str=None):


@commands.command(aliases=["sdesign", "save"])
async def savedesign(ctx, *, name:str=None):'''

