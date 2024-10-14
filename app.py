# Refactor to use get_formatted_items in the index route

import json
from flask import Flask, request, jsonify, render_template

MENU_ITEMS_FILE = 'menuitems.json'
ALLERGIES_FILE = 'allergies.json'

# Load menu items from a JSON file
def load_menu_items() -> dict:
    try:
        with open(MENU_ITEMS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Load allergy information from a JSON file
def load_allergies() -> dict:
    try:
        with open(ALLERGIES_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Format menu items for display
def get_formatted_items(menu_items: dict) -> list:
    sorted_menu_items: list[tuple[str]] = sorted(menu_items.items())
    return [f"{name}: {', '.join(ingredients)}" for name, ingredients in sorted_menu_items]

# List menu items based on whether they contain specified allergens
def list_items_by_allergen_status(selected_allergies: list) -> tuple[list, list]:
    menu_items: dict = load_menu_items()
    allergy_data: dict = load_allergies()

    can_eat: list = []
    cannot_eat: list = []
    relevant_allergen_ingredients: list = []

    # Gather all ingredients that could cause allergic reactions based on the selected allergies
    for allergy in selected_allergies:
        if allergy in allergy_data:
            relevant_allergen_ingredients.extend(allergy_data[allergy])

    # Check each menu item for allergenic ingredients
    for menu_item_name, menu_item_ingredients in menu_items.items():
        if any(ingredient in relevant_allergen_ingredients for ingredient in menu_item_ingredients):
            cannot_eat.append(menu_item_name)
        else:
            can_eat.append(menu_item_name)

    return cannot_eat, can_eat

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    allergies: list = list(load_allergies().keys())
    menu_items: dict = load_menu_items()
    filtered_menu: list = []

    if request.method == 'POST':
        selected_allergies = request.form.getlist('allergies')
        
        # Validate if any allergies were selected
        if not selected_allergies:
            selected_allergies: list = []  # If none, default to an empty list

        # Use list_items_by_allergen_status to get the list of items the user can and cannot eat
        cannot_eat, can_eat = list_items_by_allergen_status(selected_allergies)

        # Filter the items the user can eat and format them
        for name in can_eat:
            ingredients = menu_items[name]
            filtered_menu.append({"name": name, "ingredients": ', '.join(ingredients)})
    else:
        # Format the entire menu for display using get_formatted_items
        formatted_menu_items = get_formatted_items(menu_items)
        for formatted_item in formatted_menu_items:
            name, ingredients = formatted_item.split(":")
            filtered_menu.append({"name": name.strip(), "ingredients": ingredients.strip()})

    return render_template('index.html', allergies=allergies, menu=filtered_menu)

if __name__ == '__main__':
    app.run(debug=True)
