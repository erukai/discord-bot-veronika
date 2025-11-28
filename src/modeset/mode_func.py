import os
import json

folder = "modeset"

#get dialogue file
textpath = os.path.join("src", folder, "mode_dialogue.json")

with open(textpath, "r") as f:
    textfile = json.load(f)

#get master's mode file
modepath = os.path.join("src", folder, "master_mode.json")

def current_mode():
    with open(modepath, "r") as f:
        modecheck = json.load(f)
    
    return modecheck

#---------------------------------------------------------

masterrole = "Veronika's Master"

#call in every command
def get_text(ctx):

    #if author is a master
    if any(role.name == masterrole for role in ctx.author.roles):

        #get master's current role
        modecheck = current_mode()

        mastermode = modecheck.get(str(ctx.author.id)) #will get either "master" or "normal" from database
        mode_db = textfile.get(mastermode) #will get {"HELP":{...},"INFO":{...},"JAPANESE":{...},"MASTERONLY":{...},"MISC":{...}}

    #other regular people
    else:
        mode_db = textfile.get("normal")

    return mode_db