from flask import Flask, render_template
from preprocessor import load_items
from item import Item

# Create the Flask application
app = Flask(__name__)

# Load items from the game scripts
items = load_items()

@app.route('/')
def index():
    return render_template('index.html')

from flask import Flask, render_template
from item import Item

# Create the Flask application
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')