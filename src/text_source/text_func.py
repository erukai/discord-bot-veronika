import os
import json

#get dialogue file
def text_dict(lang):
    textpath = os.path.join("src", "text_source", "dialogues", f"{lang}.json")
    with open(textpath, "r") as f:
        return json.load(f)

#get master's mode setting
def current_mode():
    modepath = os.path.join("src", "text_source", "user_setting", "mode_set.json")    
    with open(modepath, "r") as f:
        return json.load(f)

#get user's language setting
def current_lang():
    langpath = os.path.join("src", "text_source", "user_setting", "lang_set.json")
    with open(langpath, "r") as f:
        return json.load(f), langpath

#---------------------------------------------------------

def get_lang(ctx):
    
    user_id = str(ctx.author.id)

    #get user's lang setting
    langfile, langpath = current_lang()

    #get user's current language
    try:
        userlang = langfile[user_id]
    except KeyError: #user key not exist
        userlang = langfile[user_id] = "en" #en is default

        with open(langpath, "w", encoding="utf-8") as f: #update key before returning value
            json.dump(langfile, f, indent=4, ensure_ascii=False)

    return userlang


masterrole = "Veronika's Master"

def get_mode(ctx, neutral:bool=False):

    if neutral:
        mode = "neutral"
        return mode

    #if author is a master
    if any(role.name == masterrole for role in ctx.author.roles):

        #get master's current role
        modefile = current_mode()

        mode = modefile.get(str(ctx.author.id)) #will get either "master" or "normal" from database

    #other regular people
    else:
        mode = "normal"

    return mode


#call in every command
def get_text(ctx):

    userlang = get_lang(ctx)
    usermode = get_mode(ctx)

    textdict = text_dict(userlang) #get lang file first
    text_mode = textdict.get(usermode) #then get dictionary {"HELP":{...},"INFO":{...},"JAPANESE":{...}, etc.}, either master or normal.

    return text_mode


#call in commands with neutral texts
def get_text_neu(ctx):

    userlang = get_lang(ctx)
    mode_neutral = get_mode(ctx, True)

    textdict = text_dict(userlang) #get lang file first
    text_mode = textdict.get(mode_neutral) #then get dictionary {"HELP":{...},"INFO":{...},"JAPANESE":{...}, etc.}, either master or normal.

    return text_mode