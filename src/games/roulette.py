import discord
from discord.ext import commands
import asyncio
import random

#-----------------------------------------------------------

class RouletteIntro(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.user_step = {}
        self.tracked_message = {}
        self.gamedata = {}

        # Step-to-handler mapping
        self.reaction_handlers = {
            "opponent": self.choose_opponent,
            "revolver1": self.revolver_start,
            "revolver2": self.revolver_session,
            "revolver_secondshot": self.secondtrigger,
        }

    #-----------------------------------------------------------

    @commands.command(aliases=["gun"])
    async def roulette(self, ctx):
        embed = discord.Embed(
            title="Russian Roulette",
            description="Russian roulette is a lethal game of chance in which a player loads a single bullet into a revolver and pulls the trigger while pointing the gun at their own head. The risk lies in not knowing whether the bullet is in the firing chamber, making each turn potentially fatal.",
            color=discord.Color(0x800000)
        )
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/1431950377443528756/1431977483049242724/black-revolver-pistol-with-flobert-ammo-4mm-dark-wooden-background_213438-3537.jpg?ex=68ff6074&is=68fe0ef4&hm=d708288c22681a2c7aa5287607eb1ef63d1f6804f82e3cdbcd360c4dd145c968&=&format=webp&width=783&height=523")
        embed.add_field(name="How to Play", value="One bullet is loaded into a single chamber, the cylinder is spun to randomize its position, and each player takes turns pointing the gun at their own head and pulling the trigger", inline=True)
        embed.add_field(name="Number of Players", value="2", inline=True)
        embed.set_footer(text="React to the emoji below to play.")

        message = await ctx.send(embed=embed)
        await message.add_reaction("🎮")  # Bot reacts to its own embed

        # Store message ID and author for next step
        self.user_step[ctx.author.id] = "opponent"
        self.tracked_message[ctx.author.id] = message.id


    #-----------------------------------------------------------


    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        print("Reaction detected:", reaction.emoji)

        if user.bot:
            return

        if reaction.message.id != self.tracked_message.get(user.id):
            print("Message ID mismatch:", reaction.message.id, "!=", self.tracked_message.get(user.id))
            return

        step = self.user_step.get(user.id)
        handler = self.reaction_handlers.get(step)
        print("Step:", step, "Handler:", handler)

        if handler:
            await handler(reaction, user)


    async def choose_opponent(self, reaction, user):
        embed = discord.Embed(
            title="Choose your Opponent",
            description="Choose who you want to play against.",
            color=discord.Color(0x800000)
        )
        embed.add_field(name="Me!", value="1️⃣", inline=True)
        embed.add_field(name="Other player", value="2️⃣", inline=True)

        message = await reaction.message.channel.send(embed=embed) #send embed when player react
        await message.add_reaction("1️⃣")  # Bot reacts to its own embed
        await message.add_reaction("2️⃣")

        self.user_step[user.id] = "revolver1"
        self.tracked_message[user.id] = message.id


    async def revolver_start(self, reaction, user):
        embed1 = discord.Embed(
            title="Russian Roulette: Revolver",
            description="Game will start soon...",
            color=discord.Color(0x800000)
        )
        embed1.set_author(name="Bot vs Player") 

        channel = reaction.message.channel

        await channel.send(embed=embed1)
        await asyncio.sleep(3) # Wait for 3 seconds

        await channel.send("Preparing revolver...")
        await asyncio.sleep(1)

        await channel.send("Loading the bullet...")
        await asyncio.sleep(1)

        await channel.send("Spinning the cylinder...")
        await asyncio.sleep(1)
    
        embed2 = discord.Embed(
            title="Who starts first?",
            description="Your choice.",
            color=discord.Color(0x800000)
        )
        embed2.set_author(name="Russian Roulette: Revolver")

        message = await channel.send(embed=embed2)
        await message.add_reaction("🤖")
        await message.add_reaction("👤")

        self.user_step[user.id] = "revolver2"
        self.tracked_message[user.id] = message.id


    async def revolver_session(self, reaction, user):
        
        state = self.gamedata.get(user.id)

        # Initialize state if not present
        if not state:
            bullet_chamber = random.randint(1, 6)
            state = {
                "bullet_chamber": bullet_chamber,
                "trigger": 0,
                "round": 1,
                "row": 1,
                "token": 1,
                "players": ["player", "bot"],
                "turn_index": 0
            }
            self.gamedata[user.id] = state

        trigger = state["trigger"]
        bullet_chamber = state["bullet_chamber"]

        round = state["round"]
        row = state["row"]

        turn_index = state["turn_index"]
        players = state["players"]

        current_move = players[turn_index]
        #in other words, current_move = ["player", "bot"][0]
        next_move = players[(turn_index + 1) % len(players)]
        
        #-----------------------------------------------------------

        channel = reaction.message.channel
            
        await channel.send("Slowly pulling the trigger...")
        await asyncio.sleep(3)

        trigger += 1
        state["trigger"] = trigger

        if trigger == bullet_chamber:
            await channel.send(f"POW! The bullet is in chamber {trigger}!")
            await asyncio.sleep(1)
            await channel.send(f"{current_move} dies. {next_move} wins!")
            
        else:
            await channel.send(f"Tick! The bullet is not in chamber {trigger}.")
            await asyncio.sleep(1)
            await channel.send(f"{6 - trigger} chambers left.")
            await asyncio.sleep(1)

            if current_move=="player" and row==1: #if player's turn, ask if player wants second shot [max=2 in a row]

                message = await channel.send("Would you like to take another shot?")
                await message.add_reaction("✅")
                await message.add_reaction("❎")

                self.user_step[user.id] = "revolver_secondshot"
                self.tracked_message[user.id] = message.id

                return  # Exit loop here

            if current_move=="player" and row==2:
                state["row"] = 1 #reset row to 1
                state["round"] += 1
                state["turn_index"] = (turn_index + 1) % len(players)

            elif current_move=="bot":
                state["round"] += 1
                state["turn_index"] = (turn_index + 1) % len(players)

            await channel.send("Starting next round...")
            await asyncio.sleep(3)
            await self.revolver_session(reaction, user)


    async def secondtrigger(self, reaction, user):

        state = self.gamedata.get(user.id)
        if not state:
            await reaction.message.channel.send("❌ No game session found.")
            return

        if reaction.emoji == "✅":
            # Player takes second shot
            state["row"] += 1
            # Resume same round, same player, but MAX attempt

        elif reaction.emoji == "❎":
            # Player passes
            state["row"] = 1
            state["round"] += 1
            state["turn_index"] = (state["turn_index"] + 1) % len(state["players"])
            # Next round, next player

        await self.revolver_session(reaction, user)

            












async def setup(bot):
    await bot.add_cog(RouletteIntro(bot))
