import gradio as gr
import cv2
import pandas as pd
from recipe_matcher import main_recipe_finder


mytheme = gr.themes.Ocean(
    primary_hue="fuchsia",
    secondary_hue="teal",
    neutral_hue="neutral",
)

placeholder_img = cv2.imread("./data/placeholder.jpeg")
placeholder_rgb = cv2.cvtColor(placeholder_img, cv2.COLOR_BGR2RGB)

# read ingredients dataset
df = pd.read_excel("italian gastronomic recipes dataset/foods/CSV/FoodDataset.xlsx")

def find_recipes(img_fridge, df):
    results = main_recipe_finder(img_fridge, df)
    recipes_string = "Hey! Based on what you have, these are some recipes you can make"

    link1 = results[3]
    link2 = results[4]
    link3 = results[5]

    rec1 = results[0]
    rec2 = results[1]
    rec3 = results[2]

    return recipes_string, link1, rec1, link2, rec2, link3, rec3

def start(img_fridge):
    ingredients = recognize_ingredients(img_fridge)
    recipes_string, l1, rec1, l2, rec2, l3, rec3 = find_recipes(ingredients)
    return recipes_string, gr.update(value=rec1, link=l1), gr.update(value=rec2, link=l2), gr.update(value=rec3, link=l3)

with gr.Blocks(theme=mytheme) as demo:
    gr.Markdown("## SiMagna \n\nWelcome to SiMagna! We'll help you discover some new Italian recipes, and show you that you can make a masterpiece starting from any base ingredient in your fridge and a quick stop at the supermarket.\n\nPlease upload a photo of your fridge so we can suggest a recipe from ingredients you already have.", container=True)
    #gr.Markdown("Welcome to SiMagna! We'll help you discover some new Italian recipes, and show you that you can make a masterpiece starting from any base ingredient in your fridge. Please upload a photo of your fridge so we can easily suggest a recipe from ingredients you already have")
    
    with gr.Row():
        inp = gr.Image(label='Input', value=placeholder_rgb)

        with gr.Column():
            out = gr.Text(label = 'Here you have 3 recipes you might like:', show_copy_button=True)   
            
            b_link1 = gr.Button(value="recipe1", link='link1', size="sm")
            b_link2 = gr.Button(value="recipe 2", link='link2', size="sm")
            b_link3 = gr.Button(value="recipe 3", link='link3', size="sm")
        
    with gr.Row():
        button_cook = gr.Button("Let's cook!", variant="primary")
        button_cook.click(fn = start, inputs=inp, outputs=[out, b_link1, b_link2, b_link3], show_progress='full')

        button_faster = gr.Button("Find faster recipes", variant="primary")


#demo.launch()
demo.launch(pwa=True, inbrowser=True, share=False) 


'''Gradio knows what buttons to update and in what order because:
    The order of outputs=[...] matches the order of values returned by the function.
    Gradio expects start(...) to return:
    1. A value for out (the gr.Text),
    2. A .update(...) for b_link1,
    3. A .update(...) for b_link2,
    4. A .update(...) for b_link3.

    Gradio uses positional matching — there’s no automatic linking based on variable names.
    '''