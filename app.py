"""
Author: Tom Purcell
"""

from flask import Flask, render_template
from preprocessor import load_items
from item import Item
import random

# Create the Flask application
app = Flask(__name__)

# Load items from the game scripts
items = load_items()


@app.route('/')
def index():

    # Randomly select 10 Items
    rand_items = random.sample(list(items.values()), 18)

    return render_template('index.html', rand_items=rand_items)


@app.route('/item/<int:item_id>')
def item(item_id):
    """
    Display the details of a specific item.
    """
    item = items.get(item_id)
    if not item:
        return "Item not found", 404

    return render_template('item.html', item=item)