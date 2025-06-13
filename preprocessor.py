
from item import Item

item_ids = set()  # Set with every found item id
items = {}        # Dictionary with every item id as key and the item object as value

with open("game_files/scripts/scr_initalize_weapons.gml" , 'r') as f:
    lines = f.readlines()
    
    for line in lines:

        # Skip lines that do not define a global variable
        if not line.startswith("global."):
            continue

        print(line.strip())