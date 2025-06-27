import gradio as gr
import cv2
import numpy as np

src_points = []

# Load placeholder image (you can also use a URL or a blank image if needed)
#placeholder_img = cv2.imread('placeholder')

# ASSUMPTION: ingredients returned as food_found: list[str]

def clear():
    global src_points
    src_points = []
    return 0#, placeholder_img

def on_select(value, evt: gr.EventData): 
    if len(src_points) < 4:
        src_points.append(evt._data['index']) 
    return len(src_points)

def get_ingredients(img):
    pass

def get_recipe(img):

    ingredients = get_ingredients

    dst_points = np.float32([
        [0,0],
        [0,800],
        [600,800],
        [600,0]
    ])



    src_float = np.float32(src_points)
    H = cv2.getPerspectiveTransform(src_float, dst_points)
    output_img = cv2.warpPerspective(img, H, (600,800))
    return output_img 

theme = gr.themes.Ocean(
    primary_hue="fuchsia",
    secondary_hue="cyan",
    neutral_hue="neutral",
)

with gr.Blocks(theme=theme) as demo:

    gr.Markdown('# SiMagna') # titoli
    gr.Markdown('find new fun recipes')

    coord_n = gr.Textbox(label='Number of ingredients', value=0)

    with gr.Row():
        inp = gr.Image(label='Input')
        #out = gr.Image(label='Output', value=placeholder_img)
        out = gr.Image(label='Output')
        inp.select(fn=on_select, inputs=inp, outputs=coord_n)     

    with gr.Row():
        btn = gr.Button("Let's cook!")
        btn.click(fn=get_recipe, inputs=inp, outputs=out)

        btn2 = gr.Button('Reset')
        btn2.click(fn=clear, outputs=[coord_n, out])

demo.launch(pwa=True, inbrowser=True)