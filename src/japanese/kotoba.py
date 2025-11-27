import discord
from discord.ext import commands
from datetime import datetime, timezone, timedelta

import unicodedata
import random
import asyncio

import json
import os
import re

#database path
folder = "japanese"
filename = "worddata.json"
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

#-------------------------------------------------------------------

roles = {
    "n": "noun",
    "v": "verb",
    "cpv": "compound verb",
    "auxv": "auxiliary verb",
    "adj": "adjective",
    "adv": "adverb"
}

def dict_embed(key):

    # Load the JSON database once
    db = load_db()

    data = db[key]
    romaji = data.get("romaji")
    timestamp = data.get("timestamp")

    #-----------------------------------

    meaning = data.get("meaning")
    meanings = "\n".join([f"— {item.strip()}" for item in meaning.split(",")])

    #-----------------------------------

    kanji_only = "".join([char for char in key if '\u4e00' <= char <= '\u9fff'])
    kanji_meaning = data.get("kanji").split(",")

    # Pair each kanji with its meaning
    mix = [f"{k} {m}" for k, m in zip(kanji_only, kanji_meaning)]
    kanji = ", ".join(mix)

    #-----------------------------------

    simple_role = data.get("role").split(",")
    full_role = [roles.get(role.strip(), role.strip()) for role in simple_role]
    role = ", ".join(full_role)

    #-----------------------------------

    embed = discord.Embed(title=key.capitalize(), color=discord.Color.purple())
    embed.add_field(name="Romaji", value=romaji, inline=True)
    embed.add_field(name="Role", value=role, inline=True)

    embed.add_field(name="Meaning", value=meanings, inline=False)
    embed.add_field(name="Kanji Meaning", value=kanji, inline=False)

    embed.set_footer(text=f"Added: {timestamp}")

    return embed

#-------------------------------------------------------------------

@commands.has_role("Veronika's Master")
@commands.command(aliases=["kotoba", "koto"])
async def entry(ctx, *, message:str=None):
    if message is None:
        embed = discord.Embed(
            title="Syntax:",
            description="`=entry [word]; [romaji]; [part of speech]; [word meaning]; [kanji meaning]; [note]`",
            color=discord.Color.purple())
        
        embed.add_field(name="Command separators:", value="`_` `;` `+` `|` `[new line]`", inline=False)
        embed.add_field(name="Word Meaning parentheses:", value="`()` : not seperated, used to add further detail of the meaning\n`[]` : seperated, used to state the concept or field of the meaning", inline=False)
        embed.add_field(name="Note separator:", value="`|` : add a new line", inline=False)
        embed.add_field(name="Aliases", value="`=kotoba`, `=koto`", inline=False)
        
        embed.set_footer(text="Word must be Japanese with at least 1 kanji!")
        await ctx.send(embed=embed)
        return

    input = message
    values = [item.strip() for item in re.split(r"[_;+|\n]+", input)]

    keys = ["word", "romaji", "role", "meaning", "kanji", "note"]

    #check if input values are complete
    if len(values) not in (5, 6):
        await ctx.send("Master, you must enter the correct number of values!")
        await ctx.send(f"`input given: {len(values)}; expected 5 or 6`")
        return

    #check if the word has kanji. If not, stop the func and throw a warning
    has_kanji = any('\u4e00' <= char <= '\u9fff' for char in values[0])
    if has_kanji:
        kanji_only = "".join([char for char in values[0] if '\u4e00' <= char <= '\u9fff'])
    else:
        await ctx.send("Master, the word must have kanji!")
        return

    kanji_meanings = [item.strip() for item in values[4].split(",")]

    #check if the num of kanji meanings is equal to kanji given
    if len(kanji_only) != len(kanji_meanings):
        await ctx.send("Master, you must enter the correct number of kanji / kanji meanings!")
        return
    
    # Check romaji notations
    romaji = values[1]
    if not any(notation in romaji for notation in [".", "-"]): 
        await ctx.send("Master, you forgot to write the notations for romaji!")
        return

    # Add empty note implicitly, if note not given
    if len(values) == 5:
        values.append("")

    addedtime = datetime.now(timezone(timedelta(hours=8))).strftime("%d-%m-%Y %H:%M")
    keys.append("timestamp")

    # Zip all the data into a dictionary
    word_data = dict(zip(keys, values))

    # Load database
    try:
        db = load_db()
    except FileNotFoundError:
        db = {}
    
    mainkey = values[0]  # The word itself

    # Preserve timestamp if the word already exists
    if mainkey in db:
        word_data["timestamp"] = db[mainkey].get("timestamp", addedtime)
    else:
        word_data["timestamp"] = addedtime

    # Add or update the entry
    db[mainkey] = word_data

    # Write updated data back to file
    with open(path, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4, ensure_ascii=False)

    await ctx.send(f"Master, the word {mainkey} has been recorded!")

    embed=dict_embed(mainkey)
    note = db[mainkey].get("note").replace("|", "\n").strip()
    if note:
        embed.add_field(name="Note", value=note, inline=False)
    await ctx.send(embed=embed)

#-------------------------------------------------------------------

@commands.has_role("Veronika's Master")
@commands.command(aliases=["dict"])
async def dictionary(ctx, *, word:str=None):
    if word is None:
        embed = discord.Embed(
            title="Syntax:",
            description="`=dictionary [word]`",
            color=discord.Color.purple())      
        embed.add_field(name="Alias", value="`=dict`")
        embed.set_footer(text="The dictionary will return the word, romaji, role, meaning, kanji meaning, and any notes.")
        await ctx.send(embed=embed)
        return

    key = word

    # Load the JSON database once
    db = load_db()

    if key in db:
        embed=dict_embed(key)
        note = db[key].get("note").replace("|", "\n").strip()
        if note:
            embed.add_field(name="Note", value=note, inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"Master, the word {word} is not in my database...")
        return


#-------------------------------------------------------------------

@commands.has_role("Veronika's Master")
@commands.command(aliases=["vocab", "vq"])
async def vocabquiz(ctx, *, filter=None):
    if filter is None:
        rounds = 10
        role_filter = None
        kanjicount = None

    else: #parse input
        arguments = [item.strip() for item in re.split(r"[\s,;]+", filter)] #will give a list of [{rounds}, {role}, {kanjicount}]

        try:
            arguments = [int(arg) if arg.isdigit() else arg for arg in arguments]
        except ValueError:
            await ctx.send("Master, I couldn't understand one of your filters.")
            return

        if len(arguments) == 3:
            rounds, role_filter, kanjicount = arguments

        elif len(arguments) == 2 and all(isinstance(arg, int) for arg in arguments): #all are int, i.e. no role
            rounds = arguments[0]
            role_filter = None
            kanjicount = arguments[1]

        elif len(arguments) == 2 and any(isinstance(arg, str) for arg in arguments): #at least one of the two is str, i.e. have role
            if isinstance(arguments[0], str): #no rounds
                rounds = 10
                role_filter = arguments[0]
                kanjicount = arguments[1]
            else: #first index is not a string, i.e. role = arguments[0], i.e. no kanjicount
                rounds = arguments[0]
                role_filter = arguments[1]
                kanjicount = None
        
        elif len(arguments) == 1 and isinstance(arguments[0], str):
            rounds = 10
            role_filter = arguments[0]
            kanjicount = None

        elif len(arguments) == 1 and isinstance(arguments[0], int):
            rounds = arguments[0]
            role_filter = None
            kanjicount = None

        elif len(arguments) > 3:
            await ctx.send(f"Master, there are only 3 filters, but you inputted {len(arguments)}!")
            return

    timeout = 20

    # load DB
    db = load_db()

    # New database of kanji count
    new_word_db = db

    # make a new dictionary of keys that satisfy both roles and kanji count.
    def is_kanji(char):
        return 'CJK UNIFIED IDEOGRAPH' in unicodedata.name(char, '')

    def kanji_count(word):
        return sum(1 for char in word if is_kanji(char))

    new_word_db = {
        key: value for key, value in db.items()
        if (
            (kanjicount is None or kanji_count(key) == kanjicount)
            and
            (role_filter is None or any(role.strip() in role_filter for role in value.get("role", "").split(",")))
        )
    }

    print(f"{rounds} {role_filter} {kanjicount}")

    #get full role name to be used in starting embed [ONLY IF ROLE IS PROVIDED]
    if role_filter is not None:
        full_role_filter = [roles.get(role.strip(), role.strip()) for role in role_filter]
        role_filter = ", ".join(full_role_filter)
    

    new_word_list = list(new_word_db.keys())
    if not new_word_list:
        await ctx.send("Master, I couldn't find any words matching your filters.")
        return

    #-------------------------------------------------------------------------

    # session intro
    embed = discord.Embed(
        title="Vocabulary Quiz",
        description=f"{ctx.author.mention}, starting a {rounds}-round vocabulary quiz! You have {timeout}s per question.",
        color=discord.Color.purple()
    )
    embed.add_field(name="Rounds", value=rounds)
    embed.add_field(name="Role", value=role_filter)
    embed.add_field(name="Kanji Count", value=kanjicount)
    embed.add_field(name="Answer Syntax:", value="`[romaji], [meaning (any)]`", inline=False)

    await ctx.send(embed=embed)
    await asyncio.sleep(3)

    score = 0
    used_keys = set()

    end_session = False
    for i in range(1, rounds + 1):
        available_keys = [k for k in new_word_list if k not in used_keys]
        if not available_keys:
            await ctx.send("Master, you've exhausted all available words. Ending session early...")
            i -= 1
            break

        key = random.choice(available_keys)
        used_keys.add(key)

        romaji = new_word_db[key]["romaji"]
        clean_romaji = re.sub(r"[-.]", "", romaji)

        meaning = [m.strip().lower() for m in re.split(r"[/,;()]", new_word_db[key]["meaning"]) if m.strip()]

        simple_role = new_word_db[key]["role"].split(",")
        full_role = [roles.get(role.strip(), role.strip()) for role in simple_role]
        role = ", ".join(full_role)

        embed_answer = dict_embed(key)
        embed_answer.set_footer(text=None)

        #-------------------------------------------------------------------------

        # ask the question
        embed_question = discord.Embed(title=f"Question {i}/{rounds}", color=discord.Color.purple())
        embed_question.add_field(name="Word", value=f"{key}", inline=False)
        embed_question.add_field(name="Role", value=f"{role}", inline=False)
        embed_question.set_footer(text=f"Master, you have {timeout} seconds. Answer by typing in chat!")
        await ctx.send(embed=embed_question)

        # check: only accept messages from the command invoker, in same channel
        def check(msg: discord.Message):
            return msg.author.id == ctx.author.id and msg.channel.id == ctx.channel.id

        answered = False
        while not answered:
            try:
                print(f"Waiting for user response... ({i})")
                reply: discord.Message = await ctx.bot.wait_for("message", timeout=timeout, check=check)
            except asyncio.TimeoutError:
                await ctx.send(f"Master, your time is up!")
                embed_answer.color = discord.Color(0xff0000)
                embed_answer.set_footer(text=f"meanings: {meaning}")
                await ctx.send(embed=embed_answer)
                await asyncio.sleep(5)
                break

            match reply.content:

                case "=stop":
                    end_session = True
                    break

                case "=skip":
                    await ctx.send(f"Master, you skipped the question!")
                    embed_answer.color = discord.Color(0xff0000)
                    embed_answer.set_footer(text=f"Meanings: {meaning}")
                    await ctx.send(embed=embed_answer)
                    await asyncio.sleep(5)
                    break

                case _ if "," not in reply.content:
                    await ctx.send("Master, please answer using the format: `[romaji], [meaning]`")
                    continue

            # got an answer from the command user
            answer_text = [part.strip() for part in reply.content.split(",", 1)]
            answer_romaji = answer_text[0]
            answer_meaning = answer_text[1]

            # Basic equality check (case-insensitive). You can replace with fuzzy match if you want.
            if answer_romaji.lower() == clean_romaji.lower() and any(word in answer_meaning.lower() for word in meaning):
                score += 1
                embed_answer.color = discord.Color.green()
                embed_answer.set_footer(text=f"Meanings: {meaning}")
                await ctx.send(f"✅ Correct! Master's score: {score}/{i}")
                await ctx.send(embed=embed_answer)
                await asyncio.sleep(5)
                answered = True

            elif answer_romaji.lower() == clean_romaji.lower() and not any(word in answer_meaning.lower() for word in meaning):
                await ctx.send(f"❌ Master, only the romaji is correct! The meaning is wrong!")

            elif not answer_romaji.lower() == clean_romaji.lower() and any(word in answer_meaning.lower() for word in meaning):
                await ctx.send(f"❌ Master, only the meaning is correct! The romaji is wrong!")

            else:
                await ctx.send(f"❌ Master, you answer is incorrect! Try again!")

        if end_session:
            break
    
    # quiz finished
    percentage = round(score / i * 100)

    embed_final = discord.Embed(title="Final score:", description=f"**{score} of {i if key is not None else (i-1)} correct** ({percentage}%)", color=discord.Color.purple())
    embed_final.set_footer(text="Let's play again next time, Master!")
    await ctx.send("Quiz finished!")
    await ctx.send(embed=embed_final)

#-------------------------------------------------------------------

@commands.has_role("Veronika's Master")
@commands.command(aliases=["wc"])
async def wordcount(ctx):
    db = load_db()
    await ctx.send(f"The number of Japanese words in the database is {len(db)}!")

@commands.has_role("Veronika's Master")
@commands.command(aliases=["up"])
async def update(ctx, *, input:str=None):
    if input is None:
        embed = discord.Embed(
            title="Syntax:",
            description="`=update w:[word] p:[romaji] r:[role] m:[meaning] km:[kanji meaning] n:[note]`",
            color=discord.Color.purple())
        embed.add_field(name="Valid prefixes:", value="`w:` `p:` `r:` `m:` `km:` `n:`", inline=False)
        embed.add_field(name="Alias", value="`=up`", inline=False)
        
        embed.set_footer(text="'w:[word]' is required!")
        await ctx.send(embed=embed)
        return
    
    # Split into tokens
    tokens = input.split()

    # Parse tokens
    current_prefix = None
    buffer = {
        "w": [],
        "p": [],
        "r": [],
        "m": [],
        "km": [],
        "n": []
    }

    for token in tokens:
        if token.startswith(("w:", "p:", "r:", "m:", "km:", "n:")):
            prefix, value = token.split(":", 1)
            if prefix not in buffer:
                await ctx.send(f"Master, the prefix `{prefix}` is not valid!")
                return
            current_prefix = prefix
            buffer[prefix].append(value)

        elif current_prefix:
            buffer[current_prefix].append(token)

    print(f"updated buffer: {buffer}")

    # Get word
    word = buffer["w"]
    
    # Validate
    if not word:
        await ctx.send("Master, the word is required! How am I supposed to update the database if you don't tell me which word, Master?")
        return
    
    elif word and not (buffer["p"] or buffer["r"] or buffer["m"] or buffer["km"] or buffer["n"]):
        await ctx.send(f"Master, at least one prefix besides `w:` is required! What attribute of '{" ".join(buffer["w"]).strip()}' do you want to update?")
        return
    
    keyname = {
        "p" : "romaji",
        "r" : "role",
        "m" : "meaning",
        "km" : "kanji",
        "n" : "note"
    }

    # Combine truthy values only
    to_update =  {keyname[k]:" ".join(v).strip() for k,v in buffer.items() if k != "w" and v}

    #--------------------------------------------------------------------

    # Update Process

    db = load_db()
    key = " ".join(word).strip() #e.g. ['', '出来る'] -> '出来る'

    #check if word provided is in the database or not
    if key not in db:
        await ctx.send(f"Master, the word {key} is not in my database...")
        return

    data = db[key] #word, romaji, meaning, etc...

    for key in data:
        if key in to_update:
            data[key] = to_update[key]

    #Save update to database
    write_db(db)

    await ctx.send(f"The word {key} has been updated!")

    embed=dict_embed(key)
    note = data.get("note").replace("|", "\n").strip()
    if note:
        embed.add_field(name="Note", value=note, inline=False)
    await ctx.send(embed=embed)