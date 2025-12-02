import discord
from discord.ext import commands
from ..text_source.text_func import get_text0

import sys
import os
import json
    
projectFolder = os.path.abspath("../02 Character Designer/new ver")
sys.path.append(projectFolder)

db_path = os.path.join(projectFolder, "datacenter", "dataset.json")
os.makedirs(projectFolder, exist_ok=True)

with open(db_path, "r") as f:
    ds = json.load(f)
    
#-----------------------------------------------------------------

# Format note
def format(value:list): #["white", "grey", "black"]

    formatted_val = [f"- {''.join(item)}" for item in value]
    return formatted_val #["- white", "- grey", "- black"]

#-----------------------------------------------------------------

@commands.command(aliases=["attr"])
async def attributes(ctx):
    text = get_text0(ctx)["DESIGN_FIELDS"]["attributes"]
    text_head = text['header']
    text_content = text['content']

    embed = discord.Embed(
        title=text_head['title'],
        description=text_head['desc'],
        color=discord.Color.light_gray()
    )
    embed.set_author(name=text_head['author'])
    embed.set_footer(text=text_head['footer'])

    for key in ["color", "color_method", "hair", "bangs", "outfit", "textile", "accessory"]:
        embed.add_field(
            name=text_content["names"][key],
            value=text_content["values"][key],
        )

    await ctx.send(embed=embed)


@commands.command(aliases=["el"])
async def elements(ctx, attr:str=None):
    text = get_text0(ctx)["DESIGN_FIELDS"]["elements"]
    text_head = text['header']
    text_err = text['errors']

    if attr is None:
        embed = discord.Embed(
            title=text['title'],
            description=text['desc'],
            color=discord.Color.light_gray()
        )
        embed.add_field(name=text['arguments'], value=text['args_val'], inline=False)
        embed.add_field(name=text['alias'], value="`=el`")
        embed.set_footer(text=text['footer'])

        await ctx.send(embed=embed)
        return

    maps = get_text0(ctx)["DESIGN_FIELDS"]["mapping"]
    ds_mapping = maps['dataset_mapping']
    attr_mapping = maps['attr_mapping']

    if attr in ["ec", "hc", "oc"]:
        attr = "c"

    elif attr not in attr_mapping:
        await ctx.send(text_err['no_attr'])
        return

    ds_key = ds_mapping[attr]

    # Might get a list with strings, or a list with dictionaries (or both), a dictionary with lists, or a dictionary with dictionaries (or both!)
    if attr in ['hw', 'tw', 'aw', 'bw', 'fw']:
        ds_value = ds['outfits'][ds_key]

    elif attr in ['ag', 'at', 'aa', 'ab', 'af']:
        ds_value = ds['body_accessories'][ds_key]

    else:
        ds_value = ds[ds_key]
    
    embed = discord.Embed(
        title=text_head['title'].format(attr=attr_mapping[attr]),
        color=discord.Color.light_gray()
    )
    embed.set_author(name=text_head['author'])
    embed.set_footer(text=text_head['footer'] if attr == "s" else None)

    if isinstance(ds_value, dict): #this only applies to `colors` and `head_hat` since they're the only top elements with dictionary as a value.
        for key, value in ds_value.items():
            if isinstance(value, dict):
                for k, v in value.items():
                    val = format(v) # assuming the value is a list
                    embed.add_field(
                        name=f"{key}: {k}",
                        value='\n'.join(val)
                    )
            elif isinstance(value, list):
                val = format(value)
                embed.add_field(
                    name=f"{key}",
                    value='\n'.join(val)
                )

    elif isinstance(ds_value, list):
        clean_list = [] #items are in string
        dict_fields = [] #items are in tuple

        for element in ds_value:
            if isinstance(element, dict): #problematic
                #add to `clean list` but make it bold. after that, make a seperate field.
                clean_list.append(f"*[{list(element.keys())[0]}]*")
                
                for k, v in element.items(): #usually only 1 key, so it won't loop
                    val = format(v) # assuming the value is a list
                    dict_fields.append((k, '\n'.join(val))) #packing two values into a tuple
                    '''embed.add_field(
                        name=k,
                        value='\n'.join(val)
                    )'''

            elif isinstance(element, str):
                clean_list.append(element)

        val = format(clean_list)
        embed.add_field(
            name=f"{attr_mapping[attr]}",
            value='\n'.join(val)
        )
        for name, value in dict_fields:
            embed.add_field(name=name, value=value)

    await ctx.send(embed=embed)