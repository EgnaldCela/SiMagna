import numpy as np
from ultralytics import YOLO
import pandas as pd
from training import best_model

#  load trained model
try:
    model = best_model
    # model = YOLO(r"C:\Users\ctorb\Downloads\last.pt")
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
        
    # get model predictions 
    results = model.predict(image, save = False, conf = conf) # save=False to avoid saving images to disk by default
    
    food_found = []
    if results:
        result = results[0] # result[0] because we feed a single image
        if result.boxes: # check if any boxes were detected
            ingredient_IDs = result.boxes.cls.tolist()
            names = result.names
            # ensure the ID exists in the names dictionary
            food_found = [names[int(id)] for id in ingredient_IDs if int(id) in names]
    return food_found

# get ingredients from input picture of the fridge
def recognize_ingredients(model, img_fridge):
    
    # calls function above with a set confidence level
    ingredients = get_ingredients(model, img_fridge, conf=0.5) # Using conf=0.5 as in your test function

    # fix quick naming incompatability
    translation = {'Carrot': 'Carrots', 'Egg' : 'Eggs', 'Chilli' : 'Chilli Peppers', 'Pepper': 'Peppers'}
    translated_ingredients = []

    for ing in ingredients:
        if ing in translation:
            translated_ingredients.append(translation[ing])
        else:
            translated_ingredients.append(ing)

    return translated_ingredients


# matches ingredients to recipes
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
        tuple: A tuple containing data we need for each recipe
    """
    scored_recipes = []
    ingredients_to_find = [ing.lower().strip() for ing in ingredients] 

    if not ingredients_to_find:
        # return all None if no ingredients are provided
        return (None, None, None, None, None, None)

    # identify all ingredient columns dynamically
    ingredient_cols = [col for col in df.columns if col.startswith('Ingredient')]

    for index, row in df.iterrows():
        recipe_ingredients = []
        for col in ingredient_cols:
            # add non-null, non-empty ingredient names to a list
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

    # get name, link, prep time, diff and cost for every recipe
    for i, recipe in enumerate(top_3_recipes):
        recipe_names[i] = recipe['Name']
        recipe_links[i] = recipe['Link']
        prep_times[i] = recipe['Preparation Time']
        difficulties[i] = recipe['Difficulty']
        costs[i] = recipe['Cost']
    
    # format string to look good on the gradio output 
    rec1 = (
    f"RECIPE 1: {recipe_names[0]}\n"
    f"• Preparation time: {prep_times[0]}\n"
    f"• Difficulty level: {difficulties[0]}\n"
    f"• Cost: {costs[0]}"
    )

    rec2 = (
    f"\n\nRECIPE 2: {recipe_names[1]}\n"
    f"• Preparation time: {prep_times[1]}\n"
    f"• Difficulty level: {difficulties[1]}\n"
    f"• Cost: {costs[1]}"
    )

    rec3 = (
    f"\n\nRECIPE 3: {recipe_names[2]}\n"
    f"• Preparation time: {prep_times[2]}\n"
    f"• Difficulty level: {difficulties[2]}\n"
    f"• Cost: {costs[2]}"
    )

    main_string = rec1 + rec2 + rec3
    
    # return in needed format for gradio
    return (
        recipe_names[0], recipe_links[0], 
        recipe_names[1], recipe_links[1], 
        recipe_names[2], recipe_links[2], 
        main_string
    )

def main_recipe_finder(image, df):
    # recognize ingredients from the model
    ingredients = recognize_ingredients(model, image)
    # get matched recipes based on recognized ingredients
    matched_recipes = match_recipes(ingredients, df)
    return matched_recipes


