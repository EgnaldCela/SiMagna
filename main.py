import gradio as gr
import cv2
import pandas as pd
from recipe_matcher import main_recipe_finder

# Set the theme for the Gradio interface with costum colors

mytheme = gr.themes.Ocean(
    primary_hue="fuchsia",
    secondary_hue="teal",
    neutral_hue="neutral",
).set(
    body_background_fill='#fcf8fc',
    body_background_fill_dark='#140014')

# Load a placeholder image to use when no image is uploaded
placeholder_img = cv2.imread("./data/placeholder.jpeg")
# Convert the placeholder image to RGB format for Gradio compatibility
placeholder_rgb = cv2.cvtColor(placeholder_img, cv2.COLOR_BGR2RGB)

# Define the function to be executed when the button is clicked
# Update corresponding Gradio elements when recipes are found: display recipes information and make buttons visible and interactive

def find_recipes(img_fridge):
    # read ingredients dataset
    df = pd.read_excel("italian gastronomic recipes dataset/foods/CSV/FoodDataset.xlsx")
    # get matched recipes based on the uploaded image
    results = main_recipe_finder(img_fridge, df)

    # unpack results
    recipes_string = results[6] if len(results) >= 7 else None
    link1 = results[1]
    link2 = results[3]
    link3 = results[5]

    rec1 = results[0]
    rec2 = results[2]
    rec3 = results[4]

    # return the results to be displayed in the Gradio interface
    return (gr.update(label='Hey! Based on what you have, these are some recipes you can make', value=recipes_string),
            gr.update(value=rec1, link=link1, visible=True, interactive=True, variant='primary'),
            gr.update(value=rec2, link=link2, visible=True, interactive=True, variant='primary'),
            gr.update(value=rec3, link=link3, visible=True, interactive=True, variant='primary'),
            gr.update(interactive=True, variant='huggingface'))

# Create the Gradio interface
# Use Blocks to create a more structured layout with rows and columns

with gr.Blocks(theme=mytheme) as demo:
    gr.Markdown("""# Welcome to SiMagna!
                We'll help you discover some new recipes from the famous Italian website Giallo Zafferano, and show you that you can make
                a masterpiece starting from any base ingredient in your house and a quick stop at the supermarket, while also fighting food waste.
                Let your culinary experience in Italy begin!""", container=False)

    with gr.Row():

        # Create input component, with a fixed height and placeholder for aesthetical purposes 

        inp = gr.Image(label='Please upload a photo of your available ingredients so we can suggest some recipes.', value=placeholder_rgb, height=352)

        with gr.Column():

            # Create output components, not visible until the main button is clicked

            out = gr.Text(label = '', value='', show_label=True, show_copy_button=True, info="""Cost indicator of the food is a discrete interval from 1 to 5
            Difficulty indicator of the food is a discrete interval from 1 to 4 \nPreparation time of the food is expressed in minutes """)

            b_link1 = gr.Button(value="recipe 1", link='link1', size="sm", visible=False, variant='secondary', interactive=False)
            b_link2 = gr.Button(value="recipe 2", link='link2', size="sm", visible=False, variant='secondary', interactive=False)
            b_link3 = gr.Button(value="recipe 3", link='link3', size="sm", visible=False, variant='secondary', interactive=False)
        
    with gr.Row():

        # Create a Button to trigger the recipe finding function and a ClearButton to reset the inputs and outputs

        button_cook = gr.Button("Let's cook!", variant="primary")
        clear = gr.ClearButton([inp, out, b_link1, b_link2, b_link3], value="Try new ingredients", variant="secondary", visible=True, interactive=False)

        # Define which functions are to be executed when clicking the buttons, define inputs to work with and outputs to work on
        # For the clear button bring the input and output components to their original state of non visibility or non interactivity

        button_cook.click(fn = find_recipes, inputs=inp, outputs=[out, b_link1, b_link2, b_link3, clear], show_progress='full')
        clear.click(fn=lambda: [gr.update(value=placeholder_rgb),
                                gr.update(value="recipe 1", link='link1', size="sm", visible=False, variant='secondary', interactive=False),
                                gr.update(value="recipe 2", link='link2', size="sm", visible=False, variant='secondary', interactive=False),
                                gr.update(value="recipe 3", link='link3', size="sm", visible=False, variant='secondary', interactive=False),
                                gr.update(variant="secondary", visible=True, interactive=False), gr.update(label = '')],
                                outputs=[inp, b_link1, b_link2, b_link3, clear, out])


# launch demo with link available for sharing for easy use also on the mobile phone, tablet, computer
demo.launch(pwa=False, inbrowser=True, share=True) 
