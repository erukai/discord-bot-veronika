import copy

import sys
import os
import json

from random import choice as random #(return 1 random item)
from random import choices as rng #(return 1 or more item, but with weights %)
from random import randrange as rdrange #(return random number from provided range)

#---------------------------------------------------------------------------------

'''projectFolder = os.path.abspath("../02 Character Designer/new ver")
sys.path.append(projectFolder)

db_path = os.path.join(projectFolder, "datacenter", "dataset.json")
os.makedirs(projectFolder, exist_ok=True)

#CHANGED TO FILTERED_DB!!!!!!!!
with open(db_path, "r") as f:
    ds = json.load(f)'''

#---------------------------------------------------------------------------------

def gender_pick(chosen_gender):
    mapping = {
        "mix": "mix",
        "male": "male",
        "m": "male",
        "female": "female",
        "f": "female",
        "random": random(["m", "f"])
    }

    gender = mapping[chosen_gender]
    return gender


def coloring(ds, count:int=1):
    
    color = copy.deepcopy(ds["colors"]) #copy color dictionary
    color_data = []

    for _ in range(count):
        color_group = random(list(color.keys()))
        color_get = random(color[color_group])

        #add color_get to color_data
        color_data.append(color_get)

        #remove last color from the local color database
        color[color_group].remove(color_get)

        #if the color group becomes empty
        if not color[color_group]:
            del color[color_group]

    return color_data


def roulette(attr):

    # Pick a random element from an attribute (expects a value of a list (most attributes) or dictionary (head_hat))
    if isinstance(attr, list):

        item = random(attr)
        
        # If item is a string, return it directly
        if isinstance(item, str):
            return item #end loop earlier

        # If item is a dict, go one level deeper and randomize from its value (expects a SINGLE LIST)
        elif isinstance(item, dict):
            inner_key = "".join(list(item.keys()))  # Each dict inside a list has ONE key

            for element in attr:
                if inner_key in element:
                    inner_key_list = element[inner_key]
                    break
            
            item = random(inner_key_list)
        
        else:
            raise ValueError("Unsupported data type: item expected str or dict")

    elif isinstance(attr, dict):

        inner_key = random(list(attr.keys())) #expects a value of a list or dictionary (again...)

        if isinstance(attr[inner_key], list):
            item = random(attr[inner_key])

        elif isinstance(attr[inner_key], dict):
            inner_key2 = random(list(attr[inner_key].keys()))
            item = random(attr[inner_key][inner_key2])

        else:
            raise ValueError("Unsupported data type: inner_key expected list or dict")

    # Fallback for unexpected types
    else:
        raise ValueError("Unsupported data type: attr expected list or dict")
    
    return item


#=========================================================================

# [[COLORING]]

def colors(ds, weight=True):

    if weight is True:
        hair_weight = ds["hair_meth_weight"]
        eye_weight = ds["eye_meth_weight"]
    elif weight is None:
        hair_weight = eye_weight = None

    hair_colorMeth = rng(ds["hair_ColorMethods"], weights=hair_weight, k=1)[0]
    eye_colorMeth = rng(ds["eye_ColorMethods"], weights=eye_weight, k=1)[0]
    shape = None

    #eyes two color or not
    if eye_colorMeth not in ["plain eyes", "patterned pupils"]:
        eye_color = coloring(ds, 2)

    elif eye_colorMeth == "plain eyes":
        eye_color = coloring(ds)

    elif eye_colorMeth == "patterned pupils":
        eye_color = coloring(ds)
        shape = random(ds["pupil_shapes"])

    #hairs two color or not
    if hair_colorMeth != "plain hair":
        hair_color = coloring(ds, 2)
    else:
        hair_color = coloring(ds)

    #random outfit color amount
    outfit_color = coloring(ds, rdrange(1, 4))

    return eye_color, eye_colorMeth, shape, hair_color, hair_colorMeth, outfit_color


#=========================================================================

# [[DATABASE ACCESS & ATTRIBUTE RANDOMIZER]]

def outfit(ds):
    # OUTFITS
    outfits = ds["outfits"] #five sub-attributes

    #Expects a DICTIONARY. Inside the dictionary, expects keys with a value of lists or a dictionary (head_hat).
    #Inside the dictionary, expects keys with a value of lists.
    headwear = roulette(outfits["headwear"])

    #Expects a LIST. Inside the list, expects a value of strings or dictionaries.
    #Inside each dictionary, expects 1 key with a value of a list.
    topwear = roulette(outfits["topwear"])

    armwear = random(outfits["armwear"])
    bottomwear = random(outfits["bottomwear"])
    footwear = random(outfits["footwear"])

    return headwear, topwear, armwear, bottomwear, footwear

#-----------------------------------------------

def accessory(ds):
    # ACCESSORIES

    #Expects a LIST. Inside the list, expects a value of strings or a dictionary.
    #Inside the dictionary, expects 1 key with a value of a list.
    acc_hair = roulette(ds["hair_ornaments"])

    body_acc = ds["body_accessories"]
    acc_general = random(body_acc["general"])
    acc_topwear = random(body_acc["topwear"])
    acc_armwear = random(body_acc["armwear"])
    acc_bottomwear = random(body_acc["bottomwear"])
    acc_footwear = random(body_acc["footwear"])

    return acc_hair, acc_general, acc_topwear, acc_armwear, acc_bottomwear, acc_footwear

def hair(ds, weight=True):

    if weight is True:
        weight = ds["hair_symm_weight"]

    # HAIRS
    hairlength = random(ds["hair_length"])
    hairsymmetry = rng(ds["hair_symmetry"], weights=weight, k=1)[0]
    hairstyle = random(ds["hair_styles"])
    haircut = random(ds["haircuts"])

    return hairlength, hairsymmetry, hairstyle, haircut

def bangs(ds):
    # BANGS
    banglength = random(ds["bangs_length"])
    bangpos = random(ds["bangs_position"])
    bangstyle = random(ds["bangs_styles"])

    return banglength, bangpos, bangstyle

def textile(ds):
    # STYLES
    patterns = random(ds["patterns"])
    prints = random(ds["prints"])
    exotic = random(ds["exotic"])

    return patterns, prints, exotic