import gradio as gr
import cv2
import pandas as pd
from recipe_matcher import main_recipe_finder


mytheme = gr.themes.Ocean(
    primary_hue="fuchsia",
    secondary_hue="teal",
    neutral_hue="neutral",
).set(
    body_background_fill='#fcf8fc',
    body_background_fill_dark='#140014')

placeholder_img = cv2.imread("./data/placeholder.jpeg")
placeholder_rgb = cv2.cvtColor(placeholder_img, cv2.COLOR_BGR2RGB)


def find_recipes(img_fridge):
    # read ingredients dataset
    df = pd.read_excel("italian gastronomic recipes dataset/foods/CSV/FoodDataset.xlsx")

    results = main_recipe_finder(img_fridge, df)
    recipes_string = results[0]
    link1 = results[4]
    link2 = results[5]
    link3 = results[6]

    rec1 = results[1]
    rec2 = results[2]
    rec3 = results[3]

    # return recipes_string, link1, rec1, link2, rec2, link3, rec3
    return gr.update(label='Hey! Based on what you have, these are some recipes you can make', value=recipes_string), gr.update(value=rec1, link=link1, visible=True, interactive=True, variant='primary'), gr.update(value=rec2, link=link2, visible=True, interactive=True, variant='primary'), gr.update(value=rec3, link=link3, visible=True, interactive=True, variant='primary'), gr.update(interactive=True, variant='huggingface')


'''
def start(img_fridge):
    ingredients = recognize_ingredients(img_fridge)
    recipes_string, l1, rec1, l2, rec2, l3, rec3 = find_recipes(ingredients)
    return recipes_string, gr.update(value=rec1, link=l1), gr.update(value=rec2, link=l2), gr.update(value=rec3, link=l3)
'''

with gr.Blocks(theme=mytheme) as demo:
    #gr.Markdown("## SiMagna \n\nWelcome to SiMagna! We'll help you discover some new Italian recipes, and show you that you can make a masterpiece starting from any base ingredient in your fridge and a quick stop at the supermarket.\n\nPlease upload a photo of your fridge so we can suggest a recipe from ingredients you already have.", container=True)
    #gr.Markdown("Welcome to SiMagna! We'll help you discover some new Italian recipes, and show you that you can make a masterpiece starting from any base ingredient in your fridge. Please upload a photo of your fridge so we can easily suggest a recipe from ingredients you already have")
    gr.Markdown("## SiMagna")
    gr.Markdown("Welcome to SiMagna! We'll help you discover some new recipes from the famous Italian website Giallo Zafferano, and show you that you can make a masterpiece starting from any base ingredient in your fridge and a quick stop at the supermarket.\n\nPlease upload a photo of your fridge so we can suggest some recipes from ingredients you already have.", container=False)

    with gr.Row():
        inp = gr.Image(label='Input', value=placeholder_rgb, height=352)

        with gr.Column():
            #out = gr.Text(label = 'Here you have 3 recipes you might like:', show_copy_button=True)   
            out = gr.Text(label = '', value='', show_copy_button=True, info="Cost indicator of the food is a discrete interval from 1 to 5 \nDifficulty indicator of the food is a discrete interval from 1 to 4 \nPreparation time of the food is expressed in minutes ")

            b_link1 = gr.Button(value="recipe 1", link='link1', size="sm", visible=False, variant='secondary', interactive=False)
            b_link2 = gr.Button(value="recipe 2", link='link2', size="sm", visible=False, variant='secondary', interactive=False)
            b_link3 = gr.Button(value="recipe 3", link='link3', size="sm", visible=False, variant='secondary', interactive=False)
        
    with gr.Row():
        button_cook = gr.Button("Let's cook!", variant="primary")
        clear = gr.ClearButton([inp, out, b_link1, b_link2, b_link3], value="Try new ingredients", variant="secondary", visible=True, interactive=False)

        button_cook.click(fn = find_recipes, inputs=inp, outputs=[out, b_link1, b_link2, b_link3, clear], show_progress='full')

        #clear.click(fn=lambda: [None, gr.update(value="recipe 1", link='link1', size="sm", visible=True, variant='secondary', interactive=False), gr.update(visible=False), gr.update(visible=False)], outputs=[out, b_link1, b_link2, b_link3])
        #clear.click(fn=lambda: [None, gr.update(value="recipe 1", link='link1', size="sm", visible=False, variant='secondary', interactive=False), gr.update(value="recipe 2", link='link2', size="sm", visible=False, variant='secondary', interactive=False), gr.update(value="recipe 3", link='link3', size="sm", visible=False, variant='secondary', interactive=False), gr.update(variant="secondary", visible=True, interactive=False), gr.update(label = '')], outputs=[out, b_link1, b_link2, b_link3, clear, out])
        clear.click(fn=lambda: [gr.update(value=placeholder_rgb), gr.update(value="recipe 1", link='link1', size="sm", visible=False, variant='secondary', interactive=False), gr.update(value="recipe 2", link='link2', size="sm", visible=False, variant='secondary', interactive=False), gr.update(value="recipe 3", link='link3', size="sm", visible=False, variant='secondary', interactive=False), gr.update(variant="secondary", visible=True, interactive=False), gr.update(label = '')], outputs=[inp, b_link1, b_link2, b_link3, clear, out])



#demo.launch()
demo.launch(pwa=False, inbrowser=True, share=True) 


'''Gradio knows what buttons to update and in what order because:
    The order of outputs=[...] matches the order of values returned by the function.
    Gradio expects start(...) to return:
    1. A value for out (the gr.Text),
    2. A .update(...) for b_link1,
    3. A .update(...) for b_link2,
    4. A .update(...) for b_link3.

    Gradio uses positional matching — there’s no automatic linking based on variable names.
    '''