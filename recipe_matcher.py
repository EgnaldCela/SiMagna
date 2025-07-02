import numpy as np
from ultralytics import YOLO
import pandas as pd
from training import best_model

try:
    model = best_model
    #model = YOLO(r"C:\Users\ctorb\Downloads\last.pt")
    print(f"YOLO model loaded successfully from {model.model_name}")
except Exception as e:
    print(f"Error loading YOLO model: {e}")
    print("Please ensure the model file exists and is accessible.")
    model = None # Set model to None if loading fails

# write general function to get ingredients from the model
def get_ingredients(model: YOLO, image: str | np.ndarray, conf: float | None = None) -> list[str]:
    """
    Recognizes ingredients in an image using the YOLO model.
    This function is directly from  main.py.

    Args:
        model: The loaded YOLO model.
        image: The input image (path string or numpy array).
        conf: Confidence threshold for object detection.

    Returns:
        A list of recognized ingredient names.
    """
    if model is None:
        return ["Error: YOLO model not loaded. Cannot recognize ingredients."]
        
    # The .predict method is robust and handles various input formats
    results = model.predict(image, save = False, conf = conf) # save=False to avoid saving images to disk by default
    
    food_found = []
    if results:
        result = results[0] # result[0] because we feed a single image
        if result.boxes: # Check if any boxes were detected
            ingredient_IDs = result.boxes.cls.tolist()
            names = result.names
            # Ensure the ID exists in the names dictionary
            food_found = [names[int(id)] for id in ingredient_IDs if int(id) in names]
    return food_found

# get ingredients from input picture of the fridge
def recognize_ingredients(model, img_fridge):
    # calls function above with a set confidence level
    ingredients = get_ingredients(model, img_fridge, conf=0.5) # Using conf=0.5 as in your test function

    # TRANSLATION FROM LABELS TO INGREDIENT NAME IN DATASET WORKS CORRECTLY
    translation = {'Carrot': 'Carrots', 'Egg' : 'Eggs', 'Chilli' : 'Chilli Peppers', 'Pepper': 'Peppers'}
    translated_ingredients = []

    for ing in ingredients:
        if ing in translation:
            translated_ingredients.append(translation[ing])
        else:
            translated_ingredients.append(ing)

    return translated_ingredients



def match_recipes(ingredients: list, df: pd.DataFrame) -> tuple:
    """
    Matches recipes from a DataFrame based on a list of ingredients,
    prioritizing recipes with more matching ingredients.

    Args:
        ingredients (list): A list of ingredient names (strings) to search for.
        df (pd.DataFrame): The DataFrame containing recipe data.
                          Expected columns include 'Name', 'Link', and multiple
                          'Ingredient', 'Ingredient.1', ..., 'Ingredient.17' columns.

    Returns:
        tuple: A tuple containing six elements:
               (recipe_name_1, recipe_name_2, recipe_name_3,
                recipe_link_1, recipe_link_2, recipe_link_3).
               If fewer than 3 recipes are found, the corresponding name/link will be None.
    """
    scored_recipes = []
    ingredients_to_find = [ing.lower().strip() for ing in ingredients] # Normalize input ingredients

    if not ingredients_to_find:
        # Return all None if no ingredients are provided
        return (None, None, None, None, None, None)

    # Identify all ingredient columns dynamically
    ingredient_cols = [col for col in df.columns if col.startswith('Ingredient')]

    for index, row in df.iterrows():
        recipe_ingredients = []
        for col in ingredient_cols:
            # Add non-null, non-empty ingredient names to a list, normalized
            if pd.notna(row[col]) and str(row[col]).strip() != '':
                recipe_ingredients.append(str(row[col]).lower().strip())

        current_recipe_match_count = 0
        for req_ing in ingredients_to_find:
            if req_ing in recipe_ingredients:
                current_recipe_match_count += 1

        # Only consider recipes that have at least one matching ingredient
        if current_recipe_match_count > 0:
            scored_recipes.append({
                'Name': row['Name'],
                'Link': row['Link'],
                'MatchCount': current_recipe_match_count # Store match count for sorting
            })

    # Sort recipes by MatchCount in descending order
    scored_recipes.sort(key=lambda x: x['MatchCount'], reverse=True)

    # Extract the top 3 recipes (or fewer if less than 3 are found)
    top_3_recipes = scored_recipes[:3]

    # Initialize output variables with None
    recipe_name_1, recipe_name_2, recipe_name_3 = None, None, None
    recipe_link_1, recipe_link_2, recipe_link_3 = None, None, None

    # Populate variables based on found recipes
    if len(top_3_recipes) > 0:
        recipe_name_1 = top_3_recipes[0]['Name']
        recipe_link_1 = top_3_recipes[0]['Link']
    if len(top_3_recipes) > 1:
        recipe_name_2 = top_3_recipes[1]['Name']
        recipe_link_2 = top_3_recipes[1]['Link']
    if len(top_3_recipes) > 2:
        recipe_name_3 = top_3_recipes[2]['Name']
        recipe_link_3 = top_3_recipes[2]['Link']

    # FOR THE RETURN ADD FOR EACH RECIPE: difficuly, cost, preparation time

    return (recipe_name_1, recipe_name_2, recipe_name_3,
            recipe_link_1, recipe_link_2, recipe_link_3)

def main_recipe_finder(image, df):
    # recognize ingredients from the model
    ingredients = recognize_ingredients(model, image)
    matched_recipes = match_recipes(ingredients, df)
    return matched_recipes


