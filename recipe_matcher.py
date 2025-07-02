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

        # only consider recipes that have at least one matching ingredient
        if current_recipe_match_count > 0:
            scored_recipes.append({
                'Name': row['Name'],
                'Link': row['Link'],
                'Preparation Time': row.get('Preparation Time'), # get preparation time
                'Difficulty': row.get('Difficulty'),             # get difficulty level
                'Cost': row.get('Cost'),
                'MatchCount': current_recipe_match_count # store match count for sorting
            })

    # sort recipes by match count in descending order
    scored_recipes.sort(key=lambda x: x['MatchCount'], reverse=True)

    # extract the top 3 recipes
    top_3_recipes = scored_recipes[:3]

    # initialize output variables 
    recipe_names = [None] * 3
    recipe_links = [None] * 3
    prep_times = [None] * 3
    difficulties = [None] * 3
    costs = [None] * 3

    for i, recipe in enumerate(top_3_recipes):
        recipe_names[i] = recipe['Name']
        recipe_links[i] = recipe['Link']
        prep_times[i] = recipe['Preparation Time']
        difficulties[i] = recipe['Difficulty']
        costs[i] = recipe['Cost']
    
    rec1 = f"1st recipe is {recipe_names[0]} with a preparation time of {prep_times[0]},difficulty level {difficulties[0]} and cost {costs[0]}"
    rec2 = f"2nd recipe is {recipe_names[1]} with a preparation time of {prep_times[1]},difficulty level {difficulties[1]} and cost {costs[1]}"
    rec3 = f"3rd recipe is {recipe_names[2]} with a preparation time of {prep_times[2]} ,difficulty level {difficulties[2]} and cost {costs[2]}"
    main_string = rec1 + rec2 + rec3
    
    return (
        recipe_names[0], recipe_links[0], 
        recipe_names[1], recipe_links[1], 
        recipe_names[2], recipe_links[2], 
        main_string
    )

def main_recipe_finder(image, df):
    # recognize ingredients from the model
    ingredients = recognize_ingredients(model, image)
    matched_recipes = match_recipes(ingredients, df)
    return matched_recipes


