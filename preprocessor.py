"""
#
"""

import re
from item import Item

item_ids = set()  # Set with every found item id
items = {}        # Dictionary with every item id as key and the item object as value
current_id = 0    # Current item id if var i is used
ID_REGEX = r"\[(\w+)\]"
VAR_ID_REGEX = r"var\s+i\s*=\s*(\d+)"
ATTRIBUTE_REGEX = r"item_(\w+)\[\w+\]"
VALUE_REGEX = r"=\s*(.+?);"

with open("game_files/scripts/scr_initalize_weapons.gml" , 'r') as f:
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

        # Update the item with the value found in the line
        match attribute_string:
            case "type":                 items[id].type = value_string
            case "name":                 items[id].name = value_string
            case "sprite":               items[id].image = value_string
            case "damage":               items[id].damage = float(value_string)
            case "shot_speed":           items[id].shot_speed = float(value_string)
            case "fire_rate":            items[id].fire_rate = float(value_string)
            case "range":                items[id].range = float(value_string)
            case "tier":                 items[id].tier = value_string
            case "shot_number":          items[id].shot_number = int(value_string)
            case "shot_angle_increment": items[id].shot_angle = float(value_string)
            case "special":              items[id].special = value_string
            case "special_amount":       items[id].special_amount = int(value_string)
            case _:                      pass  # Ignore unknown attributes