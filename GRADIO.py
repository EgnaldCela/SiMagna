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
    recipes_string = 'here goes the text with complete info'

    # Notes: this function will return the text with the recipes and their details (you must open dataset to find ingredients, preparation time, cost,
    # LINK is also found for the recipe when opening the dataset, so since you already have the information, store the variables link1, link2, link3
    
    # put actual link of respective recipe found
    link1 = "https://ricette.giallozafferano.it/Spaghetti-alla-Carbonara.html"
    link2 = 'link of recipe 2'
    link3 = 'link of recipe 3'

    # will this be changed everytime I get new recipes? it should
   
    return recipes_string, link1, link2, link3

# maybe structure for the output string
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
    recipes_string, l1, l2, l3 = find_recipes(ingredients)

    # once we have the recipe IDs, access dataset to find missing information for output: 
    # all ingredients needed, preparation time, cost, link to recipe
    # or get full recipe detail and acces preparation time, cost and link with index?

    return recipes_string, gr.update(link=l1), gr.update(link=l2), gr.update(link=l3)

with gr.Blocks(theme=mytheme) as demo:
    gr.Markdown("## SiMagna")
    gr.Markdown("Welcome to SiMagna! We'll help you discover some new Italian recipes, and show you that you can make a masterpiece starting from any base ingredient in your fridge. Please upload a photo of your fridge so we can easily suggest a recipe from ingredients you already have")
    
    with gr.Row():
        inp = gr.Image(label='Input', value=placeholder_rgb)
        with gr.Column():
            out = gr.Text(label = 'Here you have 3 recipes you might like:', show_copy_button=True)   
            
            b_link1 = gr.Button(value="recipe1", link='link1', size="sm")
            b_link2 = gr.Button(value="recipe 2", link='link2', size="sm")
            b_link3 = gr.Button(value="recipe 3", link='link3', size="sm")
        
    with gr.Row():
                button_cook = gr.Button("Let's cook!", variant="primary")
                button_faster = gr.Button("Find faster recipes", variant="primary")

    button_cook.click(fn = start, inputs=inp, outputs=[out, b_link1, b_link2, b_link3])

    '''Gradio knows what buttons to update and in what order because:
    The order of outputs=[...] matches the order of values returned by the function.
    Gradio expects start(...) to return:
    1. A value for out (the gr.Text),
    2. A .update(...) for b_link1,
    3. A .update(...) for b_link2,
    4. A .update(...) for b_link3.

    Gradio uses positional matching — there’s no automatic linking based on variable names.
    '''

   # button_faster.click(fn = faster, inputs = inp, outputs=out)


#demo.launch()
demo.launch(pwa=True, inbrowser=True) 
