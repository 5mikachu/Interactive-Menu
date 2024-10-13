import json

MENU_ITEMS_FILE = 'menuitems.json'
ALLERGIES_FILE = 'allergies.json'

# Function to load menu items from JSON file
def load_menu_items() -> list:
    try:
        with open(MENU_ITEMS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Return an empty list if the file does not exist


# Function to load allergies from JSON file
def load_allergies() -> dict:
    try:
        with open(ALLERGIES_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}  # Return an empty dict if the file does not exist


# Function to check if a certain menu item contains allergens
import json

MENU_ITEMS_FILE = 'menuitems.json'
ALLERGIES_FILE = 'allergies.json'


# Function to load menu items from JSON file (structured as a dict)
def load_menu_items() -> dict:
    try:
        with open(MENU_ITEMS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


# Function to load allergies from JSON file
def load_allergies() -> dict:
    try:
        with open(ALLERGIES_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


# Function to check if a certain menu item contains allergens
def check_menu_item_for_allergens(menu_item_name: str) -> None:
    menu_items: dict = load_menu_items()
    allergies: dict = load_allergies()

    # Find the menu item by name (dictionary key)
    if menu_item_name not in menu_items:
        print(f"Menu item '{menu_item_name}' not found!")
        return

    # Get ingredients for the selected menu item
    menu_item_ingredients = menu_items[menu_item_name]
    allergens_found = set()

    # Check for allergens in the ingredients
    for allergen, allergen_ingredients in allergies.items():
        for ingredient in menu_item_ingredients:
            if ingredient in allergen_ingredients:
                allergens_found.add(allergen)

    # Display result
    if allergens_found:
        print(f"'{menu_item_name}' contains the following allergens: {', '.join(allergens_found)}")
    else:
        print(f"'{menu_item_name}' does not contain any known allergens.")


# Function to list menu items based on allergen status for specific allergies
def list_menu_items_by_allergen_status(allergies: str) -> None:
    menu_items: list = load_menu_items()
    all_allergies: dict = load_allergies()

    # Normalize the allergies input to always be a list
    if isinstance(allergies, str):
        allergies: str = [allergies]

    # Lists to store items the user can and can't eat
    can_eat: list = []
    cannot_eat: list = []

    # Get the list of allergen ingredients for the specified allergies
    relevant_allergen_ingredients = []
    for allergy in allergies:
        if allergy in all_allergies:
            relevant_allergen_ingredients.extend(all_allergies[allergy])

    # Check each menu item for the specified allergens
    for menu_item_name, menu_item_ingredients in menu_items.items():
        contains_allergens = False

        # Check if this item contains any of the specified allergens
        if any(ingredient in relevant_allergen_ingredients for ingredient in menu_item_ingredients):
            contains_allergens = True

        if contains_allergens:
            cannot_eat.append(menu_item_name)
        else:
            can_eat.append(menu_item_name)

    # Output the lists of menu items
    print(f"Menu items you can eat (does not contain {allergy}):")
    for item in can_eat:
        print(f"- {item}")

    print(f"\nMenu items you cannot eat (contains {allergy}):")
    for item in cannot_eat:
        print(f"- {item}")


if __name__ == "__main__":
    check_menu_item_for_allergens("Pizza")
    list_menu_items_by_allergen_status("shellfish")
