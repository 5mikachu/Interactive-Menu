# User-Friendly Restaurant Menu

## Overview

Welcome to the Allergy-Friendly Restaurant Menu! This allows users to filter restaurant menu items based on selected allergens, helping diners easily find meals they can enjoy without worry.

## Features

* Menu filtering by allergens: Select your allergens from a list, and the app will display items you can safely eat.
* Simple, intuitive interface: Checkboxes for allergens and an easy-to-read menu layout.
* Dynamic filtering: Automatically updates the menu based on your selections.

## Technologies Used

* Flask: Backend web framework.
* HTML & Jinja: Frontend templating.
* CSS: Styling (linked in static/styles.css).
* JSON: Storage for menu items and allergy data.

## How It Works

* Load the app.
* Select any allergens you want to avoid.
* Submit the form to filter the menu. Items containing the selected allergens will be excluded from the list.

## Installation & Setup

* Clone the repository.
* Install dependencies with ```pip install -r requirements.txt```.
* Run the Flask app with ```python app.py```.
* Access the app in your browser at http://127.0.0.1:5000/.