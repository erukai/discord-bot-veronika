import discord
from discord.ext import commands

import json
import os

import aiohttp
from dotenv import load_dotenv
load_dotenv()  # loads .env file into environment
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

from ..text_source.text_func import get_text, get_text_neu, get_lang

#database path
folder = "utility"
filename = "note_db.json"
path = os.path.join("src", folder, filename)

# Load database
def load_db():
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Write updated data to database
def write_db(new_data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(new_data, f, indent=4, ensure_ascii=False)

# Format note (CLIENT SIDE ONLY)
def format(notes_list):
    
    formatted_text = []
    for index, item in enumerate(notes_list):
    
        child_notes = item.split("\n", 1) #"test\n  - test 1\n  - test 2" --> ["test", "  - test 1\n  - test 2"]
        for i, item in enumerate(child_notes):

            if i == 0:
                child_notes[i] = f"{item} **[{index+1}]**\n" #"test" --> "test **[1]**\n"

            elif i == len(child_notes) - 1:
                child_notes[i] = f"{item}\n"

            else:
                continue

        formatted_text.append(f"- {"".join(child_notes)}") #["test **[1]**\n", "  - test 1\n  - test 2"] --> "- test **[1]**\n", "  - test 1\n  - test 2"

    all_notes  = "".join(formatted_text)

    return all_notes

#==============================================================

def note_embed(ctx, all_notes):
    text = get_text_neu(ctx)["UTILITY"]["note_embed"]
    name = ctx.author.name

    embed = discord.Embed(
        title=text[0],
        description=all_notes,
        color=discord.Color(0x4c3228))
    embed.set_author(name=text[1].format(author=name))
    embed.set_thumbnail(url=ctx.author.avatar)

    return embed


@commands.command(aliases=["n"])
async def note(ctx, *, text:str=None):
    text = get_text_neu(ctx)["UTILITY"]["note"]

    if text is None:
        embed = discord.Embed(
            title=text[0],
            description=text[1],
            color=discord.Color(0x4c3228))      
        embed.add_field(name=text[2], value="`=n`")
        embed.set_footer(text=text[3])
        await ctx.send(embed=embed)
        return

    user_id = str(ctx.author.id)
    note_db = load_db()

    #Update the entry. If key not exist, add to the dict and then update.
    note_db.setdefault(user_id, []).append(text)

    # Write updated data to db
    write_db(note_db)

    await ctx.send(text[4])

    #--------------------------------

    notes = note_db.get(user_id)

    #revise the index of all notes
    all_notes = format(notes)
    
    embed = note_embed(ctx, all_notes)
    await ctx.send(embed=embed)


@commands.command(aliases=["mn"])
async def mynote(ctx):
    text = get_text_neu(ctx)["UTILITY"]["mynote"]

    db = load_db()
    notes = db.get(str(ctx.author.id))
    
    #if list is falsy, i.e. empty
    if not notes:
        await ctx.send(text[0])
        return

    #revise the index of all notes
    all_notes = format(notes)
    
    embed = note_embed(ctx, all_notes)
    await ctx.send(embed=embed)


@commands.command(aliases=["dn"])
async def delnote(ctx, index:int=None):
    text = get_text_neu(ctx)["UTILITY"]["delnote"]

    if index is None:
        embed = discord.Embed(
            title=text[0],
            description=text[1],
            color=discord.Color(0x4c3228))      
        embed.add_field(name=text[2], value="`=dn`")
        embed.set_footer(text=text[3])
        await ctx.send(embed=embed)
        return
    
    db = load_db()
    user_id = str(ctx.author.id)

    notes = db.get(user_id) #will return a list. if id not found, will return None. if list empty, will return a falsy list.
    
    #if list is falsy, i.e. empty or id is None
    if not notes:
        await ctx.send(text[4])
        return

    if index > 0:
        index -= 1
    else:
        await ctx.send(text[5])
        return

    try:
        del notes[index]
        if notes:
            await ctx.send(text[6])

            db[user_id] = notes
            write_db(db)

            #revise the index of all notes
            new_notes = db.get(user_id)
            all_notes = format(new_notes)
            
            embed = note_embed(ctx, all_notes)
            await ctx.send(embed=embed)

        else:
            db[user_id] = notes
            write_db(db)
            await ctx.send(text[7])

    except IndexError:
        await ctx.send(text[8])
        return
    

@commands.command(aliases=["en"])
async def editnote(ctx, index:int=None, *, text:str=None):
    text = get_text_neu(ctx)["UTILITY"]["editnote"]

    if (index is None) or (text is None):
        embed = discord.Embed(
            title=text[0],
            description=text[1],
            color=discord.Color(0x4c3228))      
        embed.add_field(name=text[2], value="`=en`")
        embed.set_footer(text=text[3])
        await ctx.send(embed=embed)
        return

    db = load_db()
    user_id = str(ctx.author.id)

    notes = db.get(user_id)
    
    #if list is falsy, i.e. empty
    if not notes:
        await ctx.send(text[4])
        return

    if index > 0:
        index -= 1
    else:
        await ctx.send(text[5])
        return

    try:
        notes[index] = text
        
        await ctx.send(text[6])

        db[user_id] = notes
        write_db(db)

        #revise the index of all notes
        new_notes = db.get(user_id)
        all_notes = format(new_notes)
        
        embed = note_embed(ctx, all_notes)
        await ctx.send(embed=embed)

    except IndexError:
        await ctx.send(text[7])
        return


@commands.command(aliases=["wt"])
async def weather(ctx, measure:str=None, *, city:str=None):
    text = get_text_neu(ctx)["UTILITY"]["weather"]

    embed = discord.Embed(
            title=text[0],
            description=text[1],
            color=discord.Color(0x4c3228))
    embed.add_field(name=text[2], value=text[3], inline=False)
    embed.add_field(name=text[4], value="`=wt`", inline=False)

    if measure is None:
        await ctx.send(embed=embed)
        return

    elif measure.lower() not in ["metric", "m", "imperial", "i"]:
        await ctx.send(text[5])
        await ctx.send(embed=embed)
        return

    elif city is None:
        await ctx.send(text[6])
        await ctx.send(embed=embed)
        return

    async with aiohttp.ClientSession() as session:

        try:
            params = {"key": WEATHER_API_KEY, "q": city}
            url = f"http://api.weatherapi.com/v1/current.json"

            async with session.get(url, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    dataloc = data['location']
                    datanow = data['current']

                    city_name = dataloc['name']
                    region = dataloc['region']
                    country = dataloc['country']
                    localtime = dataloc['localtime']

                    condition = datanow['condition']['text']
                    condition_url = datanow['condition']['icon']

                    temp_c = datanow['temp_c']
                    temp_f = datanow['temp_f']

                    feelslike_c = datanow['feelslike_c']
                    feelslike_f = datanow['feelslike_f']

                    wind_kph = datanow['wind_kph']
                    wind_mph = datanow['wind_mph']
                    wind_dir = datanow['wind_dir']

                    precip_mm = datanow['precip_mm']
                    precip_in = datanow['precip_in']

                    humidity = datanow['humidity']
                    cloud = datanow['cloud']

                    heat_c = datanow['heatindex_c']
                    heat_f = datanow['heatindex_f']

                    uv = datanow['uv']
                
                else:
                    await ctx.send(text[7])

        except:
            await ctx.send(text[8])
            return
        
    embed = discord.Embed(
        title=text[9],
        description=condition,
        color=discord.Color(0x4c3228))
    
    embed.add_field(name="Location", value=f"- City: {city_name}\n- Region: {region}\n- Country: {country}")

    if measure.lower() in ["metric", "m"]:
        embed.add_field(name="Heat", value=f"- Temperature: {temp_c}°C\n- Feels like: {feelslike_c}°C\n- Heat Index: {heat_c}°C\n- UV Index: {uv}")
        embed.add_field(name="Water", value=f"- Precipitation: {precip_mm}mm\n- Humidity: {humidity}%\n- Cloud: {cloud}%")
        embed.add_field(name="Wind", value=f"- Wind speed: {wind_kph}kph\n- Wind direction: {wind_dir}")

    else:
        embed.add_field(name="Heat", value=f"- Temperature: {temp_f}°F\n- Feels like: {feelslike_f}°F\n- Heat Index: {heat_f}°F\n- UV Index: {uv}")
        embed.add_field(name="Water", value=f"- Precipitation: {precip_in}in\n- Humidity: {humidity}%\n- Cloud: {cloud}%")
        embed.add_field(name="Wind", value=f"- Wind speed: {wind_mph}mph\n- Wind direction: {wind_dir}")

    embed.set_thumbnail(url=f"https:{condition_url}")
    embed.set_footer(text=f"Local time: {localtime}")
    await ctx.send(embed=embed)


@commands.command(aliases=["lang"])
async def language(ctx, code:str=None):
    if code is None:
        embed = discord.Embed(
            title="Syntax:",
            description="`=language [code]`",
            color=discord.Color(0x4c3228))      
        embed.add_field(name="Available Languages", value="- English: `en`\n- Malay (Classical): `my`\n- T'kilab: `tk`", inline=False)
        embed.add_field(name="Alias", value="`=lang`")
        await ctx.send(embed=embed)
        return

    #get language file
    lang_path = os.path.join("src", "text_source", "dialogues", "lang.json")
    with open(lang_path, "r") as f:
        langcheck = json.load(f)

    user_id = (str(ctx.author.id))

    #get user's current language
    userlang = get_lang(ctx)

    if code not in ['en', 'my', 'tk']:
        embed = discord.Embed(
            title="Syntax:",
            description="`=language [code]`",
            color=discord.Color(0x4c3228))      
        embed.add_field(name="Available Languages", value="- English: `en`\n- Malay: `my`\n- T'kilab: `tk`", inline=False)
        embed.add_field(name="Alias", value="`=lang`")

        await ctx.send("Language code is not in my database!")
        await ctx.send(embed=embed)
        return

    else:
        if userlang == code:
            await ctx.send(f"Current language is already `English`!")
            return
        else:
            new_userlang = code
            await ctx.send(f"Language has been changed to `English`!")
    
    # Add or update the entry
    langcheck[user_id] = new_userlang

    # Write updated data back to file
    with open(lang_path, "w", encoding="utf-8") as f:
        json.dump(langcheck, f, indent=4, ensure_ascii=False)