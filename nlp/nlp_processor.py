import re

def process_ingredients(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z, ]', '', text)

    ingredients = text.split(',')
    ingredients = [i.strip() for i in ingredients if i.strip()]

    return ingredients
