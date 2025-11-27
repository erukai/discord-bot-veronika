import discord
from discord.ext import commands
from datetime import timedelta
import asyncio
import re

#--------------------------------------------------------------------------------

@commands.command(aliases=["mute"])
@commands.has_permissions(moderate_members=True)
async def silence(ctx, member:discord.Member=None, duration:str=None, *, reason="Not given"):
    if member is None or duration is None:
        embed = discord.Embed(
            title="Syntax:",
            description="`=silence [@user] [duration: s, m, h, d] [reason (optional)]`",
            color=discord.Color(0xff0000))
        embed.add_field(name="Alias", value="`=mute`")
        embed.set_footer(text="User must be mentioned!")
        await ctx.send(embed=embed)
        return

    if ctx.author.id == member.id: 
        await ctx.channel.send("Master, you can't silence yourself!")
        return

    if not duration:
            await ctx.send("Master, you must input the duration!")
            return
    
    # Convert duration string to timedelta
    match = re.match(r"(\d+)([smhd])", duration)
    if not match:
        await ctx.send("Master, please use a valid time format like `10s, 30m`, `2h`, or `1d`.")
        return
    
    value, unit = int(match.group(1)), match.group(2)
    delta = None

    if unit == "s":
        delta = timedelta(seconds=value)
    elif unit == "m":
        delta = timedelta(minutes=value)
    elif unit == "h":
        delta = timedelta(hours=value)
    elif unit == "d":
        delta = timedelta(days=value)

    try:
        if delta is None:
            await ctx.send("Unknown unit. Use s, m, h, or d.")
            return

        await member.timeout(delta, reason=reason)
        await ctx.send(f"{member.mention} has been silenced for {duration}! Reason: {reason}")

    except Exception as e:
        await ctx.send(f"Failed to silence: `{e}`")

@commands.command(aliases=["unmute"])
@commands.has_permissions(moderate_members=True)
async def unsilence(ctx, member:discord.Member=None):
    if member is None:
        embed = discord.Embed(
            title="Syntax:",
            description="`=unsilence [@user]`",
            color=discord.Color(0xff0000))
        embed.add_field(name="Alias", value="`=unmute`")
        embed.set_footer(text="User must be mentioned!")
        await ctx.send(embed=embed)
        return

    if member.timed_out_until:
        try:
            await member.timeout(None)
            await ctx.send(f"{member.mention} has been unsilenced!")
        except Exception as e:
            await ctx.send(f"Failed to unsilence: `{e}`")
    else:
        await ctx.send(f"{member.mention} is not currently silenced...")

#--------------------------------------------------------------------------------

@commands.command(aliases=["kick"])
@commands.has_permissions(kick_members=True)
async def smite(ctx, member:discord.Member=None, *, reason="Not given"):
    if member is None:
        embed = discord.Embed(
            title="Syntax:",
            description="`=smite [@user] [reason (optional)]`",
            color=discord.Color(0xff0000))
        embed.add_field(name="Alias", value="`=kick`")
        embed.set_footer(text="User must be mentioned!")
        await ctx.send(embed=embed)
        return

    if ctx.author.id == member.id: 
        await ctx.channel.send("Master, you can't smite yourself!")
        return

    try:
        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} has been smitten! Reason: {reason}")
    except Exception as e:
        await ctx.send(f"Failed to smite: `{e}`")

#--------------------------------------------------------------------------------

@commands.command(aliases=["ban"])
@commands.has_permissions(ban_members=True)
async def banish(ctx, member:discord.Member=None, *, reason="Not given"):
    if member is None:
        embed = discord.Embed(
            title="Syntax:",
            description="`=banish [@user] [reason (optional)]`",
            color=discord.Color(0xff0000))
        embed.add_field(name="Alias", value="`=ban`")
        embed.set_footer(text="User must be mentioned!")
        await ctx.send(embed=embed)
        return

    if ctx.author.id == member.id: 
        await ctx.channel.send("Master, you can't banish yourself!")
        return

    try:
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} has been banished! Reason: {reason}")
    except Exception as e:
        await ctx.send(f"Failed to banish: `{e}`")


@commands.command(aliases=["banid"])
@commands.has_permissions(ban_members=True)
async def banishid(ctx, user_id:int=None, *, reason="Not given"):
    if user_id is None:
        embed = discord.Embed(
            title="Syntax:",
            description="`=banishid [user_id: int]`",
            color=discord.Color(0xff0000))
        embed.add_field(name="Alias", value="`=banid`")
        embed.set_footer(text="User ID must be in integer!")
        await ctx.send(embed=embed)
        return

    if ctx.author.id == user_id: 
        await ctx.channel.send("Master, you can't banish yourself!")
        return

    user = await ctx.bot.fetch_user(user_id)
    try:
        await ctx.guild.ban(user, reason=reason)
        await ctx.send(f"{user.name} has been banished! Reason: {reason}")
    except Exception as e:
        await ctx.send(f"Failed to banish user ID {user_id}: `{e}`")

@commands.command(aliases=["unban"])
@commands.has_permissions(ban_members=True)
async def unbanish(ctx, user_id:int=None):
    if user_id is None:
        embed = discord.Embed(
            title="Syntax:",
            description="`=unbanish [user_id: int]`",
            color=discord.Color(0xff0000))
        embed.add_field(name="Alias", value="`=unban`")
        embed.set_footer(text="User ID must be in integer!")
        await ctx.send(embed=embed)
        return

    user = await ctx.bot.fetch_user(user_id)
    try:
        await ctx.guild.unban(user)
        await ctx.send(f"{user.name} has been unbanished!")
    except Exception as e:
        await ctx.send(f"Failed to unbanish user ID {user_id}: `{e}`")

#--------------------------------------------------------------------------------

@commands.command(aliases=["purge"])
@commands.has_permissions(manage_messages=True)
async def burn(ctx, amount:int=None):
    if amount is None:
        embed = discord.Embed(
            title="Syntax:",
            description="`=burn [amount <= 100]`",
            color=discord.Color(0xff0000))
        embed.add_field(name="Alias", value="`=purge`")
        embed.set_footer(text="Discord only allows deleting 100 messages per instance!")
        await ctx.send(embed=embed)
        return
    
    if amount < 1 or amount > 100:
        await ctx.send("You must choose a number between 1 and 100!")
        return

    try:
        await ctx.channel.purge(limit=amount + 1)  # +1 to include the command itself
    except Exception as e:
        await ctx.send(f"Failed to burn messages: `{e}`")

@commands.command(aliases=["nuke", "ex"])
@commands.has_permissions(manage_channels=True)
async def EXPLOOOSION(ctx):
    embed = discord.Embed(
        title="**Warning!**", 
        description="Are you sure you want to wipe out this entire channel? Think of all the memories you have made!", 
        color=discord.Color(0xff0000)
    )
    embed.set_author(name="Nuke Confirmation")
    embed.set_footer(text='Reply with "yes" to confirm, "no" to cancel.')
    await ctx.send(embed=embed)

    def check(msg: discord.Message):
        return msg.author.id == ctx.author.id and msg.channel.id == ctx.channel.id

    try:
        reply: discord.Message = await ctx.bot.wait_for("message", timeout=10, check=check)
    except asyncio.TimeoutError:
        await ctx.send(f"You took too long to respond. Nuke cancelled!")
        return

    if reply.content.lower() == "yes":
        old_channel = ctx.channel
        new_channel = await old_channel.clone()

        await old_channel.delete()
        await new_channel.send("A certain crimson demon mage has nuked this channel!")

    elif reply.content.lower() == "no":
        await ctx.send("Understood. Nuke cancelled!")

    else:
        await ctx.send("Confirmation not found. Nuke cancelled!")