import discord
from discord.ext import commands

from ..background.design_calc import gender_pick, colors, outfit, accessory, hair, bangs, textile
from ..text_source.text_func import get_text0
from operator import itemgetter
from copy import deepcopy

import sys
import os
import json

#session path
folder1 = "character"
filename1 = "session.json"
seshpath = os.path.join("src", folder1, filename1)

#saved design path
folder2 = "character"
filename2 = "saved_design.json"
savedpath = os.path.join("src", folder2, filename2)

# Load session
def load_sesh_db():
    with open(seshpath, "r", encoding="utf-8") as f:
        return json.load(f)

# Write updated data to session
def write_sesh_db(session_data):
    with open(seshpath, "w", encoding="utf-8") as f:
        json.dump(session_data, f, indent=4, ensure_ascii=False)

# Load saved design database
def load_saved_db():
    with open(savedpath, "r", encoding="utf-8") as f:
        return json.load(f)

# Write updated data to saved design database
def write_saved_db(new_design):
    with open(savedpath, "w", encoding="utf-8") as f:
        json.dump(new_design, f, indent=4, ensure_ascii=False)

#=========================================================================

def load_ds():
    projectFolder = os.path.abspath("../02 Character Designer/new ver")
    sys.path.append(projectFolder)

    db_path = os.path.join(projectFolder, "datacenter", "dataset.json")
    os.makedirs(projectFolder, exist_ok=True)

    with open(db_path, "r") as f:
        return json.load(f)


def filter_ds(ctx, filter:str, valid_filters):
    filter_map = get_text0(ctx)['DESIGNER']['filter_mapping']

    #from the string argument, extract actual filters
    given_filters = [word for word in filter.split() if word in valid_filters]
    given_filters_dict = deepcopy(filter_map)
    
    #go through each key of filter map, see where current iterated filter is at the map.
    for key, value in given_filters_dict.items():
        given_filters_dict[key] = [item for item in value if item in given_filters] #only get filtered items
    
    #check if any key are FULL (i.e. remove all sub-categories).
    #only hair_ornament & topwear can remove all.
    #head_hat can be empty IF it's also removed from headwear.

    for key in ["colors", "headwear"]:
        if len(given_filters_dict[key]) == len(filter_map[key]):
            raise Exception(f"Forbidden to remove all sub-categories for {key}.")
        
    if (len(given_filters_dict['head_hat']) == len(filter_map['head_hat'])) and "head_hat" not in given_filters_dict['headwear']:
        raise Exception(f"Forbidden to remove all sub-categories for head_hat when head_hat is not removed.")

    filtered_ds = deepcopy(load_ds())

    # Note that all 'items' are keys in the dataset. That is, they are sub-categories, not the values.
    paths = {
        "colors": filtered_ds["colors"],
        "headwear": filtered_ds["outfits"]["headwear"],
        "head_hat": filtered_ds["outfits"]["headwear"]["head_hat"]
    }
    for key, target_dict in paths.items():
        for item in given_filters_dict[key]:
            del target_dict[item]

    filtered_ds['outfits']['topwear'] = [x for x in filtered_ds['outfits']['topwear'] if "item" not in x] # reassign the list instead of removing the item.
    filtered_ds['hair_ornaments'] = [x for x in filtered_ds['hair_ornaments'] if "item" not in x]

    return filtered_ds


#Calculate randomizer, while also update the session file
def parse_session(ctx, user_id, gender, w, weightless, filter, valid_filters):

    if filter is not None:
        ds = filter_ds(ctx, filter, valid_filters)
    else:
        ds = load_ds()

    sesh_db = load_sesh_db()

    col = colors(ds, w) if weightless == "true" else colors(ds)
    fit = outfit(ds)
    acc = accessory(ds)
    hairs = hair(ds, w) if weightless == "true" else hair(ds)
    bang = bangs(ds)
    tex = textile(ds)

    #assign each key in db
    c = dict(zip(['ec', 'ecm', 's', 'hc', 'hcm', 'oc'], col))
    f = dict(zip(['hw', 'tw', 'aw', 'bw', 'fw'], fit))
    a = dict(zip(['ah', 'ag', 'at', 'aa', 'ab', 'af'], acc))
    h = dict(zip(['hl', 'hsm', 'hs', 'hct'], hairs))
    b = dict(zip(['bl', 'bp', 'bs'], bang))
    t = dict(zip(['p', 'pr', 'ex'], tex))

    #write to session
    sesh_db[user_id] = {
        k: v for k, v in zip(
            ['gender', 'weightless', 'col', 'fit', 'acc', 'hair', 'bang', 'tex'], [gender, weightless, c, f, a, h, b, t]
        )
    }

    #update db
    write_sesh_db(sesh_db)

    return col, fit, acc, hairs, bang, tex


#Calculate randomizer, while also update the session file of attributes involved
def parse_special_session(ctx, user_id, gender, w, weightless, filter, valid_filters, given_prefixes):
    sesh_db = load_sesh_db()

    #assign each key in dict. This won't be written to db. It will only be used as a reference for the loop below.
    c = dict(zip(['ec', 'ecm', 's', 'hc', 'hcm', 'oc'], colors(w) if weightless == "true" else colors()))
    f = dict(zip(['hw', 'tw', 'aw', 'bw', 'fw'], outfit()))
    a = dict(zip(['ah', 'ag', 'at', 'aa', 'ab', 'af'], accessory()))
    h = dict(zip(['hl', 'hsm', 'hs', 'hct'], hair(w) if weightless == "true" else hair()))
    b = dict(zip(['bl', 'bp', 'bs'], bangs()))
    t = dict(zip(['p', 'pr', 'ex'], textile()))

    sources = {"col": c, "fit": f, "acc": a, "hairs": h, "bang": b, "tex": t}

    for prefix in given_prefixes:
        for category, source in sources.items():
            if prefix in source:
                sesh_db[user_id][category][prefix] = source[prefix]
                break  # stop once matched

    #IF GIVEN ECM AND GOT "PATTERNED PUPILS", ALSO UPDATE PUPIL SHAPE AND RETURN IT
    if 'ecm' in given_prefixes and c['ecm'] == "patterned pupils":
        sesh_db[user_id]['col']['s'] = c['s'] #in this case, 's' is surely not "None"

    #update db
    write_sesh_db(sesh_db)

#=========================================================================

@commands.command()
async def design(ctx, gender:str=None, weightless:str=None, *, filter:str=None):
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
    
    filter_map = get_text0(ctx)["DESIGNER"]["filter_mapping"] #dict
    valid_filter_args = [item for sublist in filter_map.values() for item in sublist]

    filter_embed = get_text0(ctx)["DESIGNER"]["filter_embed"]
    filter_head = filter_embed['header']
    filter_content = filter_embed['content']

    if filter is not None and not any(word in filter for word in valid_filter_args):
        embed = discord.Embed(
            title=filter_head['title'],
            description=filter_head['desc'],
            color=discord.Color.light_gray()
        )
        embed.set_footer(text=filter_head['footer'])

        for key in ["color", "headwear", "head_hat", "topwear", "hair_ornaments"]:
            embed.add_field(name=filter_content['names'][key], value=filter_content['values'][key])
        await ctx.send(embed=embed)
        return
   
    #----------------------------------------------------------------------------------

    #get randomized attributes
    col, fit, acc, hairs, bang, tex = parse_session(ctx, user_id, gender, w, weightless, filter, valid_filter_args)

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

    #if no previous session, send error
    try:
        user_sesh = sesh_db[user_id]
    except KeyError:
        await ctx.send(text_err['no_session'])
        return
    
    gender = user_sesh['gender']
    weightless = user_sesh['weightless']
    w = None #IMPORTANT: although w is assigned, it will only be used as an argument in randomizer if weightless = True

    filter_map = get_text0(ctx)["DESIGNER"]["filter_mapping"] #dict
    valid_filter_args = [item for sublist in filter_map.values() for item in sublist]
    filter = user_sesh['weightless'] #str, or None
    
    #get randomized attributes
    col, fit, acc, hairs, bang, tex = parse_session(ctx, user_id, gender, w, weightless, filter, valid_filter_args)

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



@commands.command(aliases=["rdesign", "re"])
async def redesign(ctx, *, args:str=None):
    text = get_text0(ctx)["DESIGNER"]["redesign"]
    text_err = text['errors']
    text_msg = text['messages']

    embed_text = get_text0(ctx)["DESIGNER"]["design"]
    embed_head = embed_text['header']
    embed_content = embed_text['content']

    user_id = str(ctx.author.id)

    #if no previous session, send error
    try:
        user_sesh = load_sesh_db()[user_id]
    except KeyError:
        await ctx.send(text_err['no_session'])
        return
    
    col_pre = ['ec', 'ecm', 's', 'hc', 'hcm', 'oc']
    fit_pre = ['hw', 'tw', 'aw', 'bw', 'fw']
    acc_pre = ['ah', 'ag', 'at', 'aa', 'ab', 'af']
    hair_pre = ['hl', 'hsm', 'hs', 'hct']
    bang_pre = ['bl', 'bp', 'bs']
    tex_pre = ['p', 'pr', 'ex']

    valid_prefixes = col_pre + fit_pre + acc_pre + hair_pre + bang_pre + tex_pre

    #check for prefixes in argument
    if (args is None) or not (any(word in args.split() for word in valid_prefixes)):
        embed = discord.Embed(
            title=text['title'],
            description=text['desc'],
            color=discord.Color.light_gray()
        )
        embed.set_footer(text=text['footer'])
        embed.add_field(name=text['arguments'], value=text['args_val'], inline=False)
        embed.add_field(name=text['alias'], value="`=re`")

        await ctx.send(embed=embed)
        return
    else:
        # Extract prefixes from command message
        given_prefixes = [word for word in args.split() if word in valid_prefixes]

    #if the 's' prefix is in the argument
    if "s" in given_prefixes and user_sesh["ecm"] != "patterned pupils":
        await ctx.send(text_err['prefix_unusable'])
        return

    #--------------------------------------------------------------------------------------

    gender = user_sesh['gender']
    weightless = user_sesh['weightless']
    w = None #IMPORTANT: although w is assigned, it will only be used as an argument in randomizer if weightless = True

    filter_map = get_text0(ctx)["DESIGNER"]["filter_mapping"] #dict
    valid_filter_args = [item for sublist in filter_map.values() for item in sublist]
    filter = user_sesh['weightless'] #str, or None
    
    #randomize all attributes, but only update selected ones into session database
    parse_special_session(ctx, user_id, gender, w, weightless, filter, valid_filter_args, given_prefixes)

    #for =redesign and =alterdesign, attribute values are taken directly from the updated session.
    sesh_db = load_sesh_db()

    ec, ecm, s, hc, hcm, oc = itemgetter('ec', 'ecm', 's', 'hc', 'hcm', 'oc')(sesh_db[user_id]['col'])
    hw, tw, aw, bw, fw = itemgetter('hw', 'tw', 'aw', 'bw', 'fw')(sesh_db[user_id]['fit'])
    ah, ag, at, aa, ab, af = itemgetter('ah', 'ag', 'at', 'aa', 'ab', 'af')(sesh_db[user_id]['acc'])
    hl, hsm, hs, hct = itemgetter('hl', 'hsm', 'hs', 'hct')(sesh_db[user_id]['hair'])
    bl, bp, bs = itemgetter('bl', 'bp', 'bs')(sesh_db[user_id]['bang'])
    p, pr, ex = itemgetter('p', 'pr', 'ex')(sesh_db[user_id]['tex'])

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



@commands.command(aliases=["adesign", "alt"])
async def alterdesign(ctx, *, args:str=None):
    text = get_text0(ctx)["DESIGNER"]["alterdesign"]
    text_err = text['errors']
    text_msg = text['messages']

    embed_text = get_text0(ctx)["DESIGNER"]["design"]
    embed_head = embed_text['header']
    embed_content = embed_text['content']

    user_id = str(ctx.author.id)

    #if no previous session, send error
    try:
        user_sesh = load_sesh_db()[user_id]
    except KeyError:
        await ctx.send(text_err['no_session'])
        return
    
    col_pre = ['ec', 'ecm', 's', 'hc', 'hcm', 'oc']
    fit_pre = ['hw', 'tw', 'aw', 'bw', 'fw']
    acc_pre = ['ah', 'ag', 'at', 'aa', 'ab', 'af']
    hair_pre = ['hl', 'hsm', 'hs', 'hct']
    bang_pre = ['bl', 'bp', 'bs']
    tex_pre = ['p', 'pr', 'ex']

    valid_prefixes = col_pre + fit_pre + acc_pre + hair_pre + bang_pre + tex_pre

    #check for prefixes in argument
    if (args is None) or not (any(word in args.split() for word in valid_prefixes)):
        embed = discord.Embed(
            title=text['title'],
            description=text['desc'],
            color=discord.Color.light_gray()
        )
        embed.set_footer(text=text['footer'])
        embed.add_field(name=text['arguments'], value=text['args_val'], inline=False)
        embed.add_field(name=text['alias'], value="`=re`")

        await ctx.send(embed=embed)
        return
    else:
        # Extract prefixes from command message
        given_prefixes = [word for word in args.split() if word in valid_prefixes]

    #if the 's' prefix is in the argument
    if "s" in given_prefixes and user_sesh["ecm"] != "patterned pupils":
        await ctx.send(text_err['prefix_unusable'])
        return

    #--------------------------------------------------------------------------------------

    gender = user_sesh['gender']
    weightless = user_sesh['weightless']
    w = None #IMPORTANT: although w is assigned, it will only be used as an argument in randomizer if weightless = True

    filter_map = get_text0(ctx)["DESIGNER"]["filter_mapping"] #dict
    valid_filter_args = [item for sublist in filter_map.values() for item in sublist]
    filter = user_sesh['weightless'] #str, or None
    
    #randomize all attributes, but only update selected ones into session database
    parse_special_session(ctx, user_id, gender, w, weightless, filter, valid_filter_args, given_prefixes)

    #for =redesign and =alterdesign, attribute values are taken directly from the updated session.
    sesh_db = load_sesh_db()

    ec, ecm, s, hc, hcm, oc = itemgetter('ec', 'ecm', 's', 'hc', 'hcm', 'oc')(sesh_db[user_id]['col'])
    hw, tw, aw, bw, fw = itemgetter('hw', 'tw', 'aw', 'bw', 'fw')(sesh_db[user_id]['fit'])
    ah, ag, at, aa, ab, af = itemgetter('ah', 'ag', 'at', 'aa', 'ab', 'af')(sesh_db[user_id]['acc'])
    hl, hsm, hs, hct = itemgetter('hl', 'hsm', 'hs', 'hct')(sesh_db[user_id]['hair'])
    bl, bp, bs = itemgetter('bl', 'bp', 'bs')(sesh_db[user_id]['bang'])
    p, pr, ex = itemgetter('p', 'pr', 'ex')(sesh_db[user_id]['tex'])

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





#--------------------------------------------------------------------------------------

@commands.command(aliases=["sdesign"])
async def savedesign(ctx, *, name:str=None):
    text = get_text0(ctx)["DESIGNER"]["savedesign"]
    text_err = text['errors']
    text_msg = text['messages']

    sesh_db = load_sesh_db()
    user_id = str(ctx.author.id)

    #if no previous session, send error
    try:
        user_sesh = sesh_db[user_id]
    except KeyError:
        await ctx.send(text_err['no_session'])
        return
    
    #check if saved name already exist
    saved_db = load_saved_db()

    if saved_db[user_id][name]:
        await ctx.send()
        return
    else:
        saved_db[user_id][name] = user_sesh

    #save design to save_design database
    write_saved_db(saved_db)

    #remove session
    del sesh_db[user_id]
    write_sesh_db(sesh_db)

    await ctx.send(text_msg['success'])