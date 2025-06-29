"""
This module contains functions to load items from the game scripts.
Author: Tom Purcell
"""

import os
import re
import xml.etree.ElementTree as et  # Handles sprite files
from item import Item

def load_items() -> dict[int, Item]:
    """
    Load items from the game scripts and returns a dictionary of Item objects.
    """

    item_ids = set()  # Set with every found item id
    items = {}        # Dictionary with every item id as key and the item object as value
    current_id = 0    # Current item id if var i is used
    item_files = ["scr_initalize_helmets", "scr_initalize_rings", "scr_initalize_special",
                "scr_initalize_weapons", "scr_initialize_misc", "scr_initialize_pets",
                "scr_initialize_potions"]

    ID_REGEX = r"\[(\w+)\]"
    VAR_ID_REGEX = r"var\s+i\s*=\s*(\d+)"
    ATTRIBUTE_REGEX = r"item_(\w+)\[\w+\]"
    VALUE_REGEX = r"=\s*(.+?)(?:;|\s*$)"

    for item_file in item_files:
        with open(f"game_files/scripts/{item_file}.gml" , 'r') as f:
            lines = f.readlines()
            
            # Interate through each line in the script
            for line in lines:

                # Set the current item id
                if line.startswith("var i = "):
                    match = re.search(VAR_ID_REGEX, line)
                    if not match:
                        raise ValueError(f"No item ID in line: {line.strip()}")
                    current_id = int(match.group(1))

                # Skip lines that do not define a global variable
                if not line.startswith("global."): continue

                # Extract the item ID from the line
                match = re.search(ID_REGEX, line)
                if not match:
                    raise ValueError(f"No item ID in line: {line.strip()}")
                if match.group(1) == 'i':
                    id = current_id
                else:
                    id = int(match.group(1))
                
                # Create an item object
                if id not in item_ids:
                    item_ids.add(id)
                    items[id] = Item(id)

                # Extract the item attribute and value from the line
                match = re.search(ATTRIBUTE_REGEX, line)
                if not match:
                    raise ValueError(f"No item attribute in line: {line.strip()}")
                attribute_string = match.group(1)
                match = re.search(VALUE_REGEX, line)
                if not match:
                    raise ValueError(f"No item value in line: {line.strip()}")
                value_string = match.group(1)

                # Remove quotes from the value string if present
                value_string = value_string.strip('"\'')

                # Update the item with the value found in the line
                match attribute_string:
                    case "type":                 items[id].type = value_string
                    case "name":                 items[id].name = value_string
                    case "damage":               items[id].damage = float(value_string)
                    case "shot_speed":           items[id].shot_speed = float(value_string)
                    case "fire_rate":            items[id].fire_rate = float(value_string)
                    case "range":                items[id].range = float(value_string)
                    case "tier":                 items[id].tier = value_string
                    case "shot_number":          items[id].shot_number = int(value_string)
                    case "shot_angle_increment": items[id].shot_angle = float(value_string)
                    case "special":              items[id].special = value_string
                    case "special_amount":       items[id].special_amount = value_string
                    case "sprite":               items[id].image = get_image_from_sprite(value_string)        
                    case _:                      pass  # Ignore unknown attributes
    
    return items


def get_image_from_sprite(sprite_name: str) -> str:

    # Get the path to the sprite file
    path = os.path.join("game_files", "sprites", f"{sprite_name}.sprite.gmx")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Sprite '{path}' not found.")
    
    # Get the element tree from the sprite file
    tree = et.parse(path)
    root = tree.getroot()

    for frame in root.findall(".//frame"):
        if frame.attrib.get("index") == "0":
            return os.path.basename(frame.text)