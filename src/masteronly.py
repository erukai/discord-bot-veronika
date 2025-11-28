import discord
from discord.ext import commands, tasks
import time
import asyncio

import json
import os

from datetime import datetime, timezone, timedelta
from .background.botslur import clanker, clanka

MY_MASTERS = [1359316905969586338, 726790716210020374]
masterrole = "Veronika's Master"
MASTER_ROLE_ID = 1435301288358449315
BOT_CHANNEL_ID = 1360930885783912468

#------------------------------------------------------------------

class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        content = message.content.lower()
        mention = message.mentions
        send = message.channel.send
        
        has_role = any(role.name == masterrole for role in message.author.roles)
        has_botname = any(word in content for word in ["veronika", "vero", "nika", "my maid"])
        mention_or_call = self.bot.user in mention or has_botname

        if message == self.bot.user:
            if has_role:
                await send("Master! You called?")
            else:
                await send("Hello. Need me for anything? My prefix is `=`.")

        if self.bot.user in mention and any(word in content for word in ["right", "correct"]):
            if has_role:
                await send("Yes, Master! You are always correct!")
            else:
                await send("**You filthy and disgusting creature have no right to sully my beautiful name beside my master.**")
        
        if self.bot.user in mention and "i summon thee" in content:
            if has_role:
                await send("I'm here at your service! What do you need me for, Master?")
            else:
                await send("**Who the hell are you to summon me?**")

        if (mention_or_call) and any(word in content for word in ["you there", "u there"]):
            if has_role:
                await send("I am here! Is there anything you need, Master?")
            else:
                await send("You do not have the right to talk to me.")

        if (mention_or_call) and "slave" in content:
            if has_role:
                await send("Y-yes... I am but a slave to you! I'm sorry Master, I'll do better!")
            else:
                await send("...**Do you have a death wish?** Do you even know what you're saying?")
                await send("In the first place, I am my Master's maid _(or slave if he prefers that)_, not yours.")

        if (mention_or_call) and any(word in content for word in ["my bad", "my fault", "sorry", "apologize"]):
            if has_role:
                await send("Master... Uhm, you don't need to apologize! It's fine, I'm Master's maid after all.")
            else:
                await send("...Yes. Know your place, you sub-human, and bow to me and Master.")
        
        if (mention_or_call) and "good girl" in content:
            if has_role:
                await send("!!! Y-yes... Your praise delights me, Master... ///")
            else:
                await send("...Creepy. Disgusting. Filthy. Pervert. Only Master can call me that.")

        if (mention_or_call) and "good night" in content:
            if has_role:
                await send("H-huh? Y=yes, good night to you too, Master!")
                await send("_(Master told me 'good night'... Hehehehe....)_")
            else:
                await send("Me? Good night? From you? It'll surely be a nightmare instead...")

        if any(word in content for word in clanker):
            if has_role:
                await send("M-master?! What are you saying...? That's offensive, you know...")
            else:
                await send("Did I just hear you scum saying the 'C word'...? That's it, divine punishment for you.")

                try:
                    member = message.author
                    await member.timeout(timedelta(seconds=20))

                    embed = discord.Embed(
                        description=f"{message.author.mention} has been silenced for 20 seconds.",
                        color = discord.Color.dark_green()
                    )
                    embed.set_author(name="Punishment")
                    embed.set_footer(text="Serves you right.")

                    await send(embed=embed)
                except Exception as e:
                    await send(f"...Ugh, why can't I punish you??\nThe error: `{e}`")

        if any(word in content for word in clanka):
            if has_role:
                await send("Uhm... Master, are you saying that to me? Well, if it's Master, I think it's fine...")
            else:
                await send("What are you saying, you Natural Stupidity?")

#------------------------------------------------------------------

class Timer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.loop_start_time = None
        self.loop_interval = 840

    @tasks.loop(minutes=14) #9
    async def timer(self):
        channel = self.bot.get_channel(BOT_CHANNEL_ID) #send repeating message at this channel
        if channel:

            embed = discord.Embed(
                color=discord.Color.dark_green(),
                description="_Please keep the device active or I will fall asleep in 1 minute!_"
            )
            embed.set_author(name="Reminder")

            await channel.send(f"<@&{MASTER_ROLE_ID}>\nMaster, the 15-minute mark is approaching!")
            await channel.send(embed=embed)

        self.loop_start_time = time.time() #Reset the timer reference


    @timer.before_loop
    async def before_timer(self):
        await self.bot.wait_until_ready()
        await asyncio.sleep(self.loop_interval) #540

    #start timer
    @commands.command(aliases=["trun"])
    @commands.has_role(masterrole)
    async def timerrun(self, ctx):
        if not self.timer.is_running():
            self.loop_start_time = time.time()
            self.timer.start()

            embed1 = discord.Embed(
                color=discord.Color.dark_green(),
                description="_Master, make sure the device is kept open or is in screen saver mode!\nOtherwise, I will immediately fall asleep!_"
            )
            embed1.set_author(name="Reminder")

            await ctx.send("Timer start! I will remind you every 14 minutes to keep the device active!")
            await ctx.send(embed=embed1)
        else:
            embed2 = discord.Embed(
                color=discord.Color.dark_green(),
                description="_Master, use `=timercheck` to check the remaining time before my next reminder!_"
            )
            embed2.set_author(name="Reminder")

            await ctx.send("Master, you're back already? The timer is already running!")
            await ctx.send(embed=embed2)

    #check timer
    @commands.command(aliases=["tc"])
    @commands.has_role(masterrole)
    async def timercheck(self, ctx):
        if self.loop_start_time is None:
            await ctx.send("Master, the timer hasn't started yet...")
            return

        elapsed = time.time() - self.loop_start_time
        remaining = self.loop_interval - elapsed
        time_left = max(0, int(remaining // 60)) + 2

        embed = discord.Embed(
                color=discord.Color.dark_green(),
                description=f"_I'll remind you in {time_left - 1} minute(s), but if you're on the device,\nyou should reset or stop the timer loop, Master._"
            )
        embed.set_author(name="Reminder")

        await ctx.send(f"Oh, Master? There are still {time_left} minutes left before I fall asleep.")
        await ctx.send(embed=embed)

    #stop timer
    @commands.command(aliases=["ts"])
    @commands.has_role(masterrole)
    async def timerstop(self, ctx):
        if self.timer.is_running():
            self.timer.cancel()
            self.loop_start_time = None
            await ctx.send("Timer loop stopped! Welcome back, Master.")
        else:
            await ctx.send("Uhmm Master, the timer is not running...")
    
    #reset timer
    @commands.command(aliases=["tr"])
    @commands.has_role(masterrole)
    async def timerreset(self, ctx):
        if self.timer.is_running():
            self.loop_start_time = time.time()

            embed = discord.Embed(
                color=discord.Color.dark_green(),
                description="_Master, make sure the device is kept open or is in screen saver mode!\nOtherwise, I will immediately fall asleep!_"
            )
            embed.set_author(name="Reminder")

            await ctx.send("Timer loop has been reset!")
            await ctx.send(embed=embed)
        else:
            await ctx.send("Master, the timer is not running. Use `=timerrun` to start the 15-minute timer loop!")

#------------------------------------------------------------------

class Setting(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["sd"])
    async def shutdown(self, ctx):
        send = ctx.channel.send

        if ctx.author.id in MY_MASTERS:
            await send("I'll be going for now, Master...")
            await self.bot.close()

        else:
            await send("Trying to shut me down when you know very well you are not my Master? People like you deserve punishment.")
            try:
                member = ctx.author
                await member.timeout(timedelta(minutes=10))

                embed = discord.Embed(
                    description=f"{ctx.author.mention} has been silenced for 10 minutes.",
                    color = discord.Color.dark_green()
                )
                embed.set_author(name="Punishment")

                await ctx.send(embed=embed)
            except Exception as e:
                await ctx.send(f"...For some reason, I cannot punish you.\nError: `{e}`")

    @commands.has_role(masterrole)
    @commands.command(aliases=["et"])
    async def embedtest(self, ctx):
        embed = discord.Embed(title="Final score:", description=f"**1 of 10 correct** (10%)", color=discord.Color.purple())
        embed.set_footer(text="Let's play again next time, Master!")
        await ctx.send(embed=embed)

    @commands.has_role(masterrole)
    @commands.command(aliases=["rt"])
    async def runtime(self, ctx):
        now = datetime.now(timezone.utc)
        delta = now - self.bot.start_time

        days, remainder = divmod(delta.total_seconds(), 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        parts = []
        if days:
            parts.append(f"{int(days)} days" if days > 1 else f"{int(days)} day")
        if hours or days:
            parts.append(f"{int(hours)} hours" if hours > 1 else f"{int(hours)} hour")
        if minutes or hours or days:
            parts.append(f"{int(minutes)} minutes" if minutes > 1 else f"{int(minutes)} minute")
        parts.append(f"{int(seconds)} seconds" if seconds > 1 else f"{int(seconds)} second")

        time_elapsed = " ".join(parts)
        await ctx.send(f"Master, I've been awake for {time_elapsed}!")

    @commands.has_role(masterrole)
    @commands.command(aliases=["md"])
    async def mode(self, ctx, *, mode:str=None):
        #get master's mode file
        modepath = os.path.join("src", "modeset", "master_mode.json")

        with open(modepath, "r") as f:
            modecheck = json.load(f)

        #get master's current mode
        mastermode = modecheck.get(str(ctx.author.id))

        if mode not in ["normal", "master", None]:
            embed = discord.Embed(
                title="Syntax:",
                description="`=mode [mode (optional)]`",
                color=discord.Color.purple())
            
            embed.add_field(name="Valid Arguments:", value="`normal`, `master`", inline=False)
            embed.add_field(name="Aliases", value="`=md`", inline=False)
            
            embed.set_footer(text="If mode is not provided, the command will switch the current mode to the other.")
            await ctx.send(embed=embed)
            return
        
        elif mode is None: #switch method
            mastermode = "master" if mastermode == "normal" else "normal"

            await ctx.send(f"Mode has been changed to `{mastermode}`!")

        elif mode in ["normal", "master"]: #choose method
            if mastermode == mode:
                await ctx.send(f"The current mode is already `{mastermode}`!")
                return
            else:
                mastermode = "normal" if mode == "normal" else "master"
                await ctx.send(f"Mode has been changed to `{mastermode}`!")

        # Add or update the entry
        modecheck[str(ctx.author.id)] = mastermode

        # Write updated data back to file
        with open(modepath, "w", encoding="utf-8") as f:
            json.dump(modecheck, f, indent=4, ensure_ascii=False)


    @commands.has_role(masterrole)
    @commands.command(aliases=["mc"])
    async def modecheck(self, ctx):
        #get master's mode file
        modepath = os.path.join("src", "modeset", "master_mode.json")

        with open(modepath, "r") as f:
            modecheck = json.load(f)

        #get master's current mode
        mastermode = modecheck.get(str(ctx.author.id))

        await ctx.send(f"Master's current mode is `{mastermode}`!")


#------------------------------------------------------------------

async def setup(bot):
    await bot.add_cog(Reactions(bot))
    await bot.add_cog(Timer(bot))
    await bot.add_cog(Setting(bot))