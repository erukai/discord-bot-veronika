import discord
from discord.ext import commands

import json
import os

import aiohttp
from dotenv import load_dotenv
load_dotenv()  # loads .env file into environment
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

#database path
folder = "utility"
filename = "note_db.json"
path = os.path.join("src", folder, filename)
os.makedirs(folder, exist_ok=True)

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
    notes_num = len(notes_list)

    formatted_text = []
    for index in range(notes_num):
        formatted_text.append(f"- {notes_list[index]} **[{index+1}]**")

    return formatted_text

#==============================================================

def note_embed(ctx, all_notes):
    embed = discord.Embed(
        title="Notes",
        description=all_notes,
        color=discord.Color(0x4c3228))
    embed.set_author(name=f"{ctx.author.name}'s Notes")
    embed.set_thumbnail(url=ctx.author.avatar)

    return embed


@commands.command(aliases=["n"])
async def note(ctx, *, text:str=None):
    if text is None:
        embed = discord.Embed(
            title="Syntax:",
            description="`=note [text]`",
            color=discord.Color(0x4c3228))      
        embed.add_field(name="Alias", value="`=n`")
        embed.set_footer(text="Use =mynote to view your notes.")
        await ctx.send(embed=embed)
        return

    user_id = str(ctx.author.id)
    note_db = load_db()

    #Update the entry. If key not exist, add to the dict and then update.
    note_db.setdefault(user_id, []).append(text)

    # Write updated data to db
    write_db(note_db)

    await ctx.send("A note has been recorded!")

    #--------------------------------

    notes = note_db.get(user_id)

    #revise the index of all notes
    text_list = format(notes)
    all_notes  = "\n".join(text_list)
    
    embed = note_embed(ctx, all_notes)
    await ctx.send(embed=embed)


@commands.command(aliases=["mn"])
async def mynote(ctx):
    db = load_db()
    notes = db.get(str(ctx.author.id))
    
    #if list is falsy, i.e. empty
    if not notes:
        await ctx.send("You do not have any notes!")
        return

    #revise the index of all notes
    text_list = format(notes)
    all_notes  = "\n".join(text_list)
    
    embed = note_embed(ctx, all_notes)
    await ctx.send(embed=embed)


@commands.command(aliases=["dn"])
async def delnote(ctx, index:int=None):
    if index is None:
        embed = discord.Embed(
            title="Syntax:",
            description="`=delnote [index: int]`",
            color=discord.Color(0x4c3228))      
        embed.add_field(name="Alias", value="`=dn`")
        embed.set_footer(text="'index' is the position of the note (note 1, note 2, etc.)")
        await ctx.send(embed=embed)
        return
    
    db = load_db()
    user_id = str(ctx.author.id)

    notes = db.get(user_id) #will return a list. if list not found, will return None. if list empty, will return a falsy list.
    
    #if list is falsy, i.e. empty
    if not notes:
        await ctx.send("You do not have any notes!")
        return

    if index > 0:
        index -= 1
    else:
        await ctx.send("Index must be at least 1")
        return

    try:
        del notes[index]
        if notes:
            await ctx.send("A note has been removed!")

            db[user_id] = notes
            write_db(db)

            #revise the index of all notes
            new_notes = db.get(user_id)
            text_list = format(new_notes)
            all_notes  = "\n".join(text_list)
            
            embed = note_embed(ctx, all_notes)
            await ctx.send(embed=embed)

        else:
            db[user_id] = notes
            write_db(db)
            await ctx.send("All notes have been removed!")

    except IndexError:
        await ctx.send("Index provided is more than the number of notes!")
        return
    

@commands.command(aliases=["en"])
async def editnote(ctx, index:int, *, text:str=None):
    if text is None:
        embed = discord.Embed(
            title="Syntax:",
            description="`=note [text]`",
            color=discord.Color(0x4c3228))      
        embed.add_field(name="Alias", value="`=n`")
        embed.set_footer(text="Use =mynote to view your notes.")
        await ctx.send(embed=embed)
        return

    user_id = str(ctx.author.id)
    note_db = load_db()

    #Update the entry. If key not exist, add to the dict and then update.
    note_db.setdefault(user_id, []).append(text)

    # Write updated data to db
    write_db(note_db)

    await ctx.send("A note has been recorded!")

    #--------------------------------

    notes = note_db.get(user_id)

    #revise the index of all notes
    text_list = format(notes)
    all_notes  = "\n".join(text_list)
    
    embed = note_embed(ctx, all_notes)
    await ctx.send(embed=embed)


@commands.command(aliases=["wt"])
async def weather(ctx, measure:str=None, *, city:str=None):

    embed = discord.Embed(
            title="Syntax:",
            description="`=weather [measurement] [city]`",
            color=discord.Color(0x4c3228))
    embed.add_field(name="`[measurement]` Arguments", value="`metric` / `m`, `imperial` / `i`", inline=False)
    embed.add_field(name="Alias", value="`=wt`", inline=False)

    if measure is None:
        await ctx.send(embed=embed)
        return

    elif measure.lower() not in ["metric", "m", "imperial", "i"]:
        await ctx.send("`[measurement]` argument is not valid!`]")
        await ctx.send(embed=embed)
        return

    elif city is None:
        await ctx.send("`[city]` argument is required!")
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
                    await ctx.send(f"Sorry! Couldn't fetch weather data... `Error Code: {resp.status}`")

        except:
            await ctx.send("An error has occured! Make sure the city name is correct!")
            return
        
    embed = discord.Embed(
        title="Current Weather",
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
