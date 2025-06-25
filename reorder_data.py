import os
import shutil
import random
from ultralytics.data.utils import visualize_image_annotations
import yaml

# rest of the datasets, already structured, need to be merged

relevant_datasets = {
    # 5 classes, so many pictures for not much actually
    "food-detection-5": ['apple', 'banana', 'cabbage', 'capsicum', 'tomato'],
    # 94 classes
    "Food-Item-Detection-1": ['Apple', 'Banana', 'Beans', 'Capsicum', 'Carrot', 'Cucumber', 'Curli-Flower', 'Orange', 'Tomato', 'Tomatos', 'apple', 'asparagus', 'avocado', 'banana', 'beef', 'bell_pepper', 'bento', 'blueberries', 'bottle', 'bread', 'broccoli', 'butter', 'can', 'carrot', 'cauliflower', 'cheese', 'chicken', 'chicken_breast', 'chocolate', 'coffee', 'corn', 'cucumber', 'egg', 'eggs', 'energy_drink', 'fish', 'flour', 'garlic', 'goat_cheese', 'grapes', 'grated_cheese', 'green_beans', 'ground_beef', 'guacamole', 'ham', 'heavy_cream', 'humus', 'juice', 'ketchup', 'kothmari', 'leek', 'lemon', 'lettuce', 'lime', 'mango', 'marmelade', 'mayonaise', 'milk', 'mushrooms', 'mustard', 'nuts', 'onion', 'orange', 'pak_choi', 'parsley', 'peach', 'pear', 'pineapple', 'plasticsaveholder', 'pot', 'potato', 'potatoes', 'pudding', 'red_cabbage', 'red_grapes', 'rice_ball', 'salad', 'sandwich', 'sausage', 'shrimp', 'smoothie', 'spinach', 'spring_onion', 'strawberries', 'sugar', 'sweet_potato', 'tea_a', 'tea_i', 'tomato', 'tomato_sauce', 'tortillas', 'turkey', 'watermelon', 'yogurt'],
    # 138 classes
    "Grocery1-1": ['-', 'Apple', 'Artichoke', 'Asparagus', 'Avocado', 'Banana', 'Beans', 'Beetroot', 'Blackberries', 'Blueberries', 'Book', 'Broccoli', 'Brussel Sprouts', 'Butter', 'Cabbage', 'Cantaloupe', 'Carrots', 'Cauliflower', 'Cerealbox', 'Cheese', 'Clementine', 'Coffee', 'Corn', 'Cucumber', 'Detergent', 'Drinks', 'Egg', 'Eggplant', 'Eggs', 'Fish', 'Galia', 'Grapes', 'Honeydew', 'Juice', 'Lemon', 'Lettuce', 'Meat', 'Milk', 'Mushroom', 'Mushrooms', 'Nectarine', 'Onion', 'Orange', 'Oranges', 'Peas', 'Pineapple', 'Plum', 'Pomegranate', 'Potato', 'Raspberries', 'Salad', 'Sauce', 'Shallot', 'Spinach', 'Squash', 'Strawberries', 'Strawberry', 'Sweetcorn', 'Tofu', 'Tomato', 'Tomatoes', 'Watermelon', 'Yogurt', 'Zucchini', 'apple', 'apples', 'asparagus', 'aubergine', 'bacon', 'banana', 'bananas', 'bazlama', 'beef', 'blueberries', 'bread', 'broccoli', 'butter', 'carrot', 'carrots', 'cheese', 'chicken', 'chicken_breast', 'chocolate', 'chocolate chips', 'corn', 'courgettes', 'cream', 'cream cheese', 'dates', 'eggs', 'flour', 'ginger', 'goat_cheese', 'green beans', 'green bell pepper', 'green chilies', 'green_beans', 'ground_beef', 'ham', 'heavy_cream', 'juice', 'lemon', 'lemons', 'lettuce', 'lime', 'mango', 'meat', 'milk', 'mineral water', 'mushroom', 'mushrooms', 'olive', 'olives', 'onion', 'orange', 'parsley', 'peach', 'peppers', 'potato', 'potatoes', 'red bell pepper', 'red grapes', 'red onion', 'salami', 'sauce', 'sausage', 'shrimp', 'spinach', 'spring onion', 'strawberries', 'strawberry', 'sugar', 'sweet_potato', 'tomato', 'tomato paste', 'tomatoes', 'yellow bell pepper', 'yoghurt'],
    # 16 classes
    "Pathpal-Grocery-Detector-3-2": ['Apple', 'Banana', 'Book', 'Carrots', 'Cerealbox', 'Detergent', 'Drinks', 'Egg', 'Lemon', 'Meat', 'Milk', 'Orange', 'Strawberries', 'Tomato', 'Watermelon', 'bread'],
    # 10 classes
    "Pathpal-Grocery-Detector-3-10": ['Apple', 'Banana', 'Book', 'Carrots', 'Detergent', 'Drinks', 'Lemon', 'Meat', 'Milk', 'Orange'],
    # 14 classes (initial one)
    "initial-fruit-vegetables": ['banana_wb', 'banana', 'blackberry', 'raspberry', 'lemon_wb', 'lemon', 'grapes_wb', 'grapes', 'tomato_wb', 'tomato', 'apple_wb', 'apple', 'chilli_wb', 'chilli'] # i removed the wobs
}

def get_datasets(folderpath):
    result = []
    for folder in os.listdir(folderpath): # this will be second_try
        if not os.path.isdir(f"{folderpath}/{folder}"): continue
        yamlpath = f"{folderpath}/{folder}/data.yaml"
        with open(yamlpath, "r", encoding="utf8") as yamlfile:
            data = yaml.load(yamlfile, Loader=yaml.SafeLoader)
        names = data["names"]
        result.append((folder, names))
    return result # list of tuples (dataset name, objects inside)

def get_info(folderpath):
    result = []
    for folder in os.listdir(folderpath): # this will be second_try
        if not os.path.isdir(f"{folderpath}/{folder}"): continue
        yamlpath = f"{folderpath}/{folder}/data.yaml"
        with open(yamlpath, "r", encoding="utf8") as yamlfile:
            data = yaml.load(yamlfile, Loader=yaml.SafeLoader)
        data = data[""]
        result.append((folder, data))
    return result # list of tuples (dataset name, objects inside)

def get_classes(lists: list[str]) -> list[str]:
    result = []
    for lst in lists:
        for word in lst:
            word = word.capitalize()
            if word not in result:
                result.append(word)
    return result

tot_classes = get_classes(relevant_datasets.values())

# ['Apple', 'Banana', 'Cabbage', 'Capsicum', 'Tomato', 'Beans', 'Carrot', 'Cucumber', 'Curli-flower', 'Orange', 'Tomatos', 'Asparagus', 'Avocado', 'Beef',
# 'Bell_pepper', 'Bento', 'Blueberries', 'Bottle', 'Bread', 'Broccoli', 'Butter', 'Can', 'Cauliflower', 'Cheese', 'Chicken', 'Chicken_breast', 'Chocolate',
# 'Coffee', 'Corn', 'Egg', 'Eggs', 'Energy_drink', 'Fish', 'Flour', 'Garlic', 'Goat_cheese', 'Grapes', 'Grated_cheese', 'Green_beans', 'Ground_beef', 'Guacamole',
# 'Ham', 'Heavy_cream', 'Humus', 'Juice', 'Ketchup', 'Kothmari', 'Leek', 'Lemon', 'Lettuce', 'Lime', 'Mango', 'Marmelade', 'Mayonaise', 'Milk', 'Mushrooms',
# 'Mustard', 'Nuts', 'Onion', 'Pak_choi', 'Parsley', 'Peach', 'Pear', 'Pineapple', 'Plasticsaveholder', 'Pot', 'Potato', 'Potatoes', 'Pudding', 'Red_cabbage',
# 'Red_grapes', 'Rice_ball', 'Salad', 'Sandwich', 'Sausage', 'Shrimp', 'Smoothie', 'Spinach', 'Spring_onion', 'Strawberries', 'Sugar', 'Sweet_potato', 'Tea_a',
# 'Tea_i', 'Tomato_sauce', 'Tortillas', 'Turkey', 'Watermelon', 'Yogurt', '-', 'Artichoke', 'Beetroot', 'Blackberries', 'Book', 'Brussel sprouts', 'Cantaloupe',
# 'Carrots', 'Cerealbox', 'Clementine', 'Detergent', 'Drinks', 'Eggplant', 'Galia', 'Honeydew', 'Meat', 'Mushroom', 'Nectarine', 'Oranges', 'Peas', 'Plum',
# 'Pomegranate', 'Raspberries', 'Sauce', 'Shallot', 'Squash', 'Strawberry', 'Sweetcorn', 'Tofu', 'Tomatoes', 'Zucchini', 'Apples', 'Aubergine', 'Bacon', 'Bananas',
# 'Bazlama', 'Chocolate chips', 'Courgettes', 'Cream', 'Cream cheese', 'Dates', 'Ginger', 'Green beans', 'Green bell pepper', 'Green chilies', 'Lemons', 'Mineral water',
# 'Olive', 'Olives', 'Peppers', 'Red bell pepper', 'Red grapes', 'Red onion', 'Salami', 'Spring onion', 'Tomato paste', 'Yellow bell pepper', 'Yoghurt', 'Banana_wb', 'Blackberry',
# 'Raspberry', 'Lemon_wb', 'Grapes_wb', 'Tomato_wb', 'Apple_wb', 'Chilli_wb', 'Chilli']

def transfer_to_copy(folderpath, labels, dest_path, tot_classes):
    adjusted_labels = dict()
    no_labels_files = [] # not needed, just skip similar files

    for index, label in enumerate(labels):
        adjusted_labels[str(index)] = str(tot_classes.index(label.capitalize()))

    print(folderpath, adjusted_labels)

    for subfolder in os.listdir(folderpath): # train, test, valid
        if not os.path.isdir(f"{folderpath}/{subfolder}"):
            continue
        labelspath = f"{folderpath}/{subfolder}/labels"
        imagespath = f"{folderpath}/{subfolder}/images"
        os.makedirs(f"{dest_path}/{subfolder}/labels", exist_ok = True)
        os.makedirs(f"{dest_path}/{subfolder}/images", exist_ok = True)

        for labelname in os.listdir(labelspath):
            labelfilepath = f"{labelspath}/{labelname}"
            imagename = labelname[:-3] + "jpg"
            imagefilepath = f"{imagespath}/{imagename}"
            # get content of label file
            with open(labelfilepath, "r", encoding = "utf8") as labelfile:
                lines = labelfile.readlines()
            if lines == []:
                continue
            # change content
            destlabelfile = open(f"{dest_path}/{subfolder}/labels/{labelname}", "w", encoding = "utf8")
            for line in lines:
                line = line.split(" ")
                first_int = line[0]
                new_text = " ".join([adjusted_labels[first_int]] + line[1:])
                print(new_text, file = destlabelfile, end = "") # print corrected line in new file
            destlabelfile.close()
            # shutil.copy(imagefilepath, f"{dest_path}/{subfolder}/images/{imagename}") # copy the image (only if it has labels)

def visualize_bboxes(imagepath):
    labelmap = {index:value for index, value in enumerate(tot_classes)}
    labelpath = imagepath.split("/")
    labelpath[-2] = "labels"
    labelpath[-1] = labelpath[-1][:-3] + "txt"
    labelpath = "/".join(labelpath)
    visualize_image_annotations(imagepath, labelpath, labelmap)

def fix_train_only(folderpath):
    pass
        

def merge():
    relevant_datasets = get_datasets(tempfolder) # list od tuples
    tot_classes = [x[1] for x in relevant_datasets]

    for dataset, labels in relevant_datasets.items():
        dataset_path = f"data/{dataset}"
        transfer_to_copy(dataset_path, labels, destination, tot_classes)

if __name__ == '__main__':

    destination = "merged_dataset"
    # merge()
    tempfolder = "data/second_try/zucchine-1"
    # random_image = f"{tempfolder}/train/images/" + random.choice(os.listdir(f"{tempfolder}/train/images"))
    # visualize_bboxes(random_image)
    folderpath = "data/second_try"
    print(get_info(folderpath))