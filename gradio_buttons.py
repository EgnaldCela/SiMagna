import gradio as gr
import cv2

mytheme = gr.themes.Ocean(
    primary_hue="fuchsia",
    secondary_hue="teal",
    neutral_hue="neutral",
)

placeholder_img = cv2.imread("./data/placeholder.jpeg")
placeholder_rgb = cv2.cvtColor(placeholder_img, cv2.COLOR_BGR2RGB)

def preprocess_image(img_fridge):
    # balancing ? 
    return img_fridge

def recognize_ingredients(img_fridge):
    # model
    ingredients = list()
    return ingredients

def find_recipes(ingredients):

    recipes_string = 'here goes the text with complete info'

    link1 = "https://ricette.giallozafferano.it/Spaghetti-alla-Carbonara.html"
    link2 = 'link of recipe 2'
    link3 = 'link of recipe 3'

    rec1 = 'Spaghetti alla Carbonara'
    rec2 = 'recipe 2 name'
    rec3 = 'recipe 3 name'

    return recipes_string, link1, rec1, link2, rec2, link3, rec3

def start(img_fridge):
    img_fridge = preprocess_image(img_fridge)
    ingredients = recognize_ingredients(img_fridge)
    recipes_string, l1, rec1, l2, rec2, l3, rec3 = find_recipes(ingredients)
    return recipes_string, gr.update(value=rec1, link=l1), gr.update(value=rec2, link=l2), gr.update(value=rec3, link=l3)

with gr.Blocks(theme=mytheme) as demo:
    gr.Markdown("### SiMagna \n\nWelcome to SiMagna! We'll help you discover some new Italian recipes, and show you that you can make a masterpiece starting from any base ingredient in your fridge. Please upload a photo of your fridge so we can easily suggest a recipe from ingredients you already have", container=True)
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
demo.launch(pwa=True, inbrowser=True, share=True) 
