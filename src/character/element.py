import discord
from discord.ext import commands


@commands.command(aliases=["edesign"])
async def designelements(ctx):
    embed = discord.Embed(
        title="Elements and Prefixes",
        color=discord.Color(0x808080)
    )
    embed.set_author(name="Character Design")
    embed.add_field(name="Eye", value="eye color method [ecm:]\npupil shape [ps:]")
    embed.add_field(name="Hair", value="hair color method [hcm:]\nhair length [hl:]\nhair symmetry [hsm:]\nhair style [hs:]\nhaircut [hc:]\nhair ornaments [ho:]")
    embed.add_field(name="Bangs", value="bangs length [bl:]\nbangs position [bp:]\nbangs style [bs:]")
    embed.add_field(name="Outfits", value="headwear [hw:]\ntopwear [tw:]\narmwear [aw:]\nbottomwear [bw:]\nfootwear [fw:]")
    embed.add_field(name="Body", value="general [g:]\ntop accessory [ta:]\narm accessory [aa:]\nbottom accessory [ba:]\nfoot accessory [fa:]")
    embed.add_field(name="Style", value="pattern [p:]")

    await ctx.send(embed=embed)

