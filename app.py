import json
import logging
from flask import Flask, request, render_template

def load_menu_items() -> dict:
    menu_items_files = 'menuitems.json'
    try:
        with open(menu_items_files, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logging.warning("Error loading menuitems.json")
        return {}

def load_allergies() -> dict:
    allergies_file = 'allergies.json'
    try:
        with open(allergies_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logging.warning("Error loading allergies.json")
        return {}

def get_formatted_items(menu_items: dict) -> list:
    sorted_menu_items: list[tuple[str]] = sorted(menu_items.items())
    return [f"{name}: {', '.join(ingredients)}" for name, ingredients in sorted_menu_items]

# List menu items based on whether they contain specified allergens
def list_items_by_allergen_status(selected_allergies: list) -> tuple[list, list]:
    menu_items: dict = load_menu_items()
    allergy_data: dict = load_allergies()
    can_eat: list = []
    cannot_eat: list = []
    allergen_ingredients: list = []

    for allergy in selected_allergies:
        if allergy in allergy_data:
            allergen_ingredients.extend(allergy_data[allergy])

    for menu_item, menu_item_ingredients in menu_items.items():
        if any(ingredient in allergen_ingredients for ingredient in menu_item_ingredients):
            cannot_eat.append(menu_item)
        else:
            can_eat.append(menu_item)

    return can_eat, cannot_eat

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    allergies: list = list(load_allergies().keys())
    menu_items: dict = load_menu_items()
    filtered_menu: list = []

    if request.method == 'POST':
        selected_allergies = request.form.getlist('allergies')
        
        if not selected_allergies:
            selected_allergies: list = []

        can_eat, cannot_eat = list_items_by_allergen_status(selected_allergies)

        for name in can_eat:
            ingredients = menu_items[name]
            filtered_menu.append({"name": name, "ingredients": ', '.join(ingredients)})
    else:
        formatted_menu_items = get_formatted_items(menu_items)
        for formatted_item in formatted_menu_items:
            name, ingredients = formatted_item.split(":")
            filtered_menu.append({"name": name.strip(), "ingredients": ingredients.strip()})

    return render_template('index.html', allergies=allergies, menu=filtered_menu)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    app.run(debug=False)
