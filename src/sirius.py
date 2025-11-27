import discord
from discord.ext import commands

from .background.time_now import running_time
from .background.orcus_calc import earth_to_orcus

from datetime import datetime, timezone
import re


@commands.command(aliases=["or"])
async def orcus(ctx):
    running_time()
    orcus_time = running_time()

    embed = discord.Embed(
        title="Orcus Time Now",
        color=discord.Color(0xf4abba),
        timestamp=datetime.now(timezone.utc),
    )
    embed.set_footer(text="Earth local time")
    embed.add_field(name="Orcus Standard Time (OST):", value=f"{orcus_time}", inline=False)
    embed.add_field(name="Earth Coordinated Universal Time (UTC):", value=datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M"))

    await ctx.message.delete()
    await ctx.send(embed=embed)


@commands.command(aliases=["ot"])
async def orcustime(ctx):
    running_time()
    orcus_time = running_time()

    embed = discord.Embed(
        title="Orcus Time",
        color=discord.Color(0xf4abba),
        timestamp=datetime.now(timezone.utc),
    )
    embed.set_footer(text="Earth local time")
    embed.add_field(name="Orcus Standard Time (OST):", value=f"{orcus_time}", inline=False)
    embed.add_field(name="Earth Coordinated Universal Time (UTC):", value=datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M"))

    await ctx.send(embed=embed)


@commands.command(aliases=["oc"])
async def orcuscalc(ctx, *, message:str=None):
    if message is None:
        embed = discord.Embed(
            title="Syntax:",
            description="`=orcuscalc [earth day] [earth month] [earth year]`",
            color=discord.Color(0xf4abba))
        embed.add_field(name="Valid separators:", value="` ` `,` `;` `+` `|`")
        embed.set_footer(text="Only numbers can be inputted!")

        await ctx.send(embed=embed)
        return

    times = list(re.split(r"[\s,;+|]+", message))

    #-----------------------------------------------------------

    try:
        times = [int(t) for t in times if t.strip()]
    except ValueError:
        await ctx.send("You must enter numbers only!")
        return

    #if hour not given
    if len(times) == 3:
        times.append(0)

    #if input values are incorrect
    if len(times) < 3 or len(times) > 4:
        await ctx.send("You must enter the correct number of values!")
        await ctx.send(f"`Values given: {len(times)}; expected 3 or 4`")
        return
    
    day, month, year, hour = times[:4]

    #-----------------------------------------------------------
    #Check for INVALID earth dates

    mnth30 = (4, 6, 9, 11)
    mnth31 = (1, 3, 5, 7, 8, 10, 12)
    isleap_year = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
        
    if not (0 <= hour <= 23):
        await ctx.send("Hour must be between 0 and 23!")
        return
        
    if year < 10:
        await ctx.send("Year must be at least 10 CE!")
        return
    
    if not (1 <= month <= 12):
        await ctx.send("Month must be between 1 and 12!")
        return
    
    if month == 2:
        if isleap_year and not (1 <= day <= 29):
            await ctx.send("Day of February in a leap year must be between 1 and 29!")
            return
                
        elif not isleap_year and not (1 <= day <= 28):
            await ctx.send("Day of February in a normal year must be between 1 and 28!")
            return
                
    elif month in mnth30 and not (1 <= day <= 30):
        await ctx.send("Day of the selected month must be between 1 and 30!")
        return
            
    elif month in mnth31 and not (1 <= day <= 31):
        await ctx.send("Day of the selected month must be between 1 and 31!")
        return

    #-----------------------------------------------------------

    #finally, calculation time
    earth, orcus = earth_to_orcus(day, month, year, hour)

    embed = discord.Embed(
        #title="Earth to Orcus",
        color=discord.Color(0xf4abba),
    )
    embed.set_author(name="Time Converter: Earth to Orcus")
    embed.add_field(name="Earth Coordinated Universal Time (UTC)", value=earth, inline=False)
    embed.add_field(name="Orcus Standard Time (OST)", value=orcus, inline=False)

    await ctx.send(embed=embed)