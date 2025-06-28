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
    # open dataset
    # match ingredients with corresponding IDs
    # find recipes with most ingredients
    recipes = [1, 2, 3] # first 3 recipes
    return recipes

suggestions = '''1. {recipe1_name}
Ingredients: {recipe1_ingredients}
Preparation Time: {recipe1_preparation_time}
Cost: {recipe1_cost}
2. {recipe2_name}
Ingredients: {recipe2_ingredients}
Preparation Time: {recipe2_preparation_time}
Cost: {recipe2_cost}
3. {recipe3_name}
Ingredients: {recipe3_ingredients}
Preparation Time: {recipe3_preparation_time}
Cost: {recipe3_cost}'''

def start(img_fridge):

    # preprocessing and ingredient recognition
    # input: image of fridge -> output: enhanced image of fridge
    img_fridge = preprocess_image(img_fridge)

    # feed to model and recognize ingredients
    # input: fridge image -> output: list of ingredients recognized
    ingredients = recognize_ingredients(img_fridge)

    # find recipes on dataset based on most ingredients per recipe
    # input: list of ingredients -> output: output string with recipes information
    recipes = find_recipes(ingredients)

    # once we have the recipe IDs, access dataset to find missing information for output: 
    # all ingredients needed, preparation time, cost, link to recipe
    # or get full recipe detail and acces preparation time, cost and link with index?

    return suggestions


with gr.Blocks(theme=mytheme) as demo:
    gr.Markdown("## SiMagna")
    gr.Markdown("Welcome to SiMagna! We'll help you discover some new Italian recipes, and show you that you can make a masterpiece starting from any base ingredient in your fridge. Please upload a photo of your fridge so we can easily suggest a recipe from ingredients you already have")
    with gr.Row():
        inp = gr.Image(label='Input', value=placeholder_rgb)
        with gr.Column():
            out = gr.Text(label = 'Here you have 3 recipes you might like:', show_copy_button=True)   
            
            link1 = gr.Button(value="recipe1", link="https://ricette.giallozafferano.it/Spaghetti-alla-Carbonara.html", size="sm")
            link2 = gr.Button(value="recipe 2", link="link", size="sm")
            link3 = gr.Button(value="recipe 3", link="link", size="sm")
        
    with gr.Row():
                button_cook = gr.Button("Let's cook!", variant="primary")
                button_faster = gr.Button(value="find faster recipes", variant="primary")

    button_cook.click(fn = start, inputs=inp, outputs=out)
   # button_faster.click(fn = faster, inputs = inp, outputs=out)


#demo.launch()
demo.launch(pwa=True, inbrowser=True) 
