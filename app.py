import json
import logging
from flask import Flask, request, render_template


app = Flask(__name__)


def load_json(file_name: str) -> dict:
    """
    Load a JSON file and return its contents as a dictionary

    :param file_name:
    :return:
    """
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logging.warning(f"Error loading {file_name}")
        return {}


def get_formatted_items(menu_items: dict) -> list[dict]:
    """
    Format menu items as a list of dictionaries

    :param menu_items:
    :return:
    """
    return [{"name": name, "ingredients": ', '.join(details['ingredients']), "price": details['price']} for name, details in sorted(menu_items.items())]


def list_items_by_allergen_status(selected_allergies) -> tuple[list[str], list[str]]:
    """
    List menu items by allergen status

    :param selected_allergies:
    :return:
    """
    menu_items: dict = load_json('menuitems.json')
    allergies: dict = load_json('allergies.json')
    can_eat, cannot_eat = [], []
    allergen_ingredients: list = [ingredient for allergy in selected_allergies if allergy in allergies for ingredient in allergies[allergy]]

    for name, details in menu_items.items():
        ingredients = details['ingredients']
        (cannot_eat if any(ingredient in allergen_ingredients for ingredient in ingredients) else can_eat).append(name)

    return can_eat, cannot_eat


def filter_items_by_course(menu_items, selected_course) -> dict:
    """
    Filter menu items by course

    :param menu_items:
    :param selected_course:
    :return:
    """
    if selected_course:
        return {name: details for name, details in menu_items.items() if details['course'] == selected_course}
    return menu_items


def filter_items(menu_items: dict, selected_allergies: list[str], selected_course: str) -> dict:
    """
    Filter menu items by all selected criteria

    :param menu_items:
    :param selected_allergies:
    :param selected_course:
    :return:
    """
    can_eat, _ = list_items_by_allergen_status(selected_allergies)

    # Filter by course
    filtered_items = filter_items_by_course(menu_items, selected_course)
    can_eat = {name: details for name, details in filtered_items.items() if name in can_eat}

    return can_eat


@app.route('/', methods=['GET', 'POST'])
def index():
    allergies: list[str] = list(load_json('allergies.json').keys())
    menu_items: dict = load_json('menuitems.json')
    courses: list[str] = sorted(set(details['course'] for details in menu_items.values()))

    if request.method == 'POST':
        selected_allergies: list[str] = request.form.getlist('allergies') or []
        selected_course: str = request.form.get('course') or ''
        filtered_menu_items: dict = filter_items(menu_items, selected_allergies, selected_course)
        filtered_menu: list = get_formatted_items(filtered_menu_items)
        return render_template('menu_items.html', menu=filtered_menu)

    # Render all menu items on initial load
    initial_menu: list = get_formatted_items(menu_items)
    return render_template('index.html', allergies=allergies, courses=courses, menu=initial_menu)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    app.run(debug=False)
