import os
import shutil
import random
from ultralytics.data.utils import visualize_image_annotations
import yaml
import data.old_objects as voob

# rest of the datasets, already structured, need to be merged

relevant_datasets_old = {
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
        result.append(data["val"])
    return result

def get_classes_old(lists: list[str]) -> list[str]:
    result = []
    for lst in lists:
        for word in lst:
            word = word.capitalize()
            if word not in result:
                result.append(word)
    return result

def get_classes(datasets):
    tot_classes = []
    for dataset, classes in datasets.items():
        for name in classes:
            if name not in tot_classes:
                tot_classes.append(name.capitalize())
        # tot_classes.append(classes[-1]) # append the last item if there are multiple ones <- OLD
    # [i for i in v for v in datasets.values()] # i coulden't get it right through list comprehension
    return tot_classes

global_tot_classes = get_classes({k:v for k,v in get_datasets("data/second_try")}) # names of merged2
tot_classes_old = get_classes_old(relevant_datasets_old.values()) # labels of merged_dataset

hardcoded_tot_classes = voob.smaller_list

def label_to_label_map(tot_classes = hardcoded_tot_classes):
    result: dict[str:str] = dict()
    # classes have been modified for this function
    merged_dataset_classes = voob.merged_dataset_classes
    merged2_classes = voob.merged2_classes
    for lst in [merged_dataset_classes, merged2_classes]:
        for name in lst:
            mapped = name
            if "->" in name:
                name, mapped = name.split(" -> ")
            if mapped in tot_classes:
                result[name] = mapped
            else:
                result[name] = None
    print(result)
    return result # good, this seems a working label transformer


def transform(classes, tot_classes):
    result = dict()
    name_transform = label_to_label_map() # get name mapping
    for index, label in enumerate(classes):
        name = name_transform[label.capitalize()]
        index = str(index)
        if name in tot_classes:
            result[index] = str(tot_classes.index(name)) # create index mapping
        else:
            result[index] = None
    return result # seems to work

def merge_everything(subfolders = ["train", "valid", "test"]):
    # datasets = [["data/second_try/initial-fruit-vegetables", voob.initial_list], ["data/merged_dataset", tot_classes_old], ["data/merged2", global_tot_classes]]
    datasets = get_datasets("data/second_try")      
    destination = "bigger"
    balance_count = {name:0 for name in hardcoded_tot_classes}
    for dataset, classes in datasets:
        dataset = f"data/second_try/{dataset}"
        index_map = transform(classes, hardcoded_tot_classes) # map from index to index
        # transform label to index - get None or something to recognise if label not in hardcoded classes
        print(dataset); print(classes); print(index_map)
        balance_count = transfer_to_copy2(dataset, index_map, destination, balance_count, subfolders)

    
def transfer_to_copy2(folderpath, index_map, dest_path, balance_count, subfolders):
    # print(folderpath, index_map)
    counter = 0
    errors = []
    balance_limits = {"train": 2000, "valid": 400, "test": 200}

    for subfolder in subfolders: 
    # for subfolder in os.listdir(folderpath): # train, test, valid
        # if subfolder == "test": continue # was causing problems
        if not os.path.isdir(f"{folderpath}/{subfolder}"):
            continue
        limit = balance_limits[subfolder]
        labelspath = f"{folderpath}/{subfolder}/labels"
        imagespath = f"{folderpath}/{subfolder}/images"
        os.makedirs(f"{dest_path}/{subfolder}/labels", exist_ok = True)
        os.makedirs(f"{dest_path}/{subfolder}/images", exist_ok = True)

        for labelname in os.listdir(labelspath):
            labelfilepath = f"{labelspath}/{labelname}"
            imagename = labelname[:-3] + "jpg"
            imagefilepath = f"{imagespath}/{imagename}"
            if not os.path.exists(imagefilepath): # handle errors if image doesn's exist
                errors.append(imagefilepath)
                continue
            # get content of label file
            with open(labelfilepath, "r", encoding = "utf8") as labelfile:
                lines = labelfile.readlines()
            if lines == []:
                continue
            # change content
            included = False
            for line in lines:
                line = line.split(" ")
                first_int = line[0]
                new_index = index_map[first_int]
                if new_index is not None:
                    box_added = hardcoded_tot_classes[int(new_index)]
                    if box_added in {'Olive', 'Raspberries', 'Plum', 'Brussel sprouts' 'Peas', 'Clementine', 'Blackberries', 'Ginger', 'Nuts'}: # fewer than 100 instances in training
                        continue
                    balance_count[box_added] += 1
                    if balance_count[box_added] >= limit:
                        continue # ignore the label
                    included = True # count label as included only if it really is
                    destlabelfile = open(f"{dest_path}/{subfolder}/labels/{labelname}", "a", encoding = "utf8")
                    new_text = " ".join([new_index] + line[1:])
                    print(new_text, file = destlabelfile, end = "") # print corrected line in new file
                    destlabelfile.close()
                else:
                    counter += 1
                    continue
            if included:
                shutil.copy(imagefilepath, f"{dest_path}/{subfolder}/images/{imagename}") # copy the image (only if it has labels)
    
    with open("data/various/errors.txt", "a") as f: print(errors, file = f)
    print(f"{counter} pictures have beeen ignored")
    
    return balance_count

def transfer_to_copy(folderpath, labels, dest_path, tot_classes):
    adjusted_labels = dict()
    no_labels_files = [] # not needed, just skip similar files

    for index, label in enumerate(labels):
        adjusted_labels[str(index)] = str(tot_classes.index(label.capitalize()))

    print(folderpath, adjusted_labels)
    counter = 0
    errors = []

    for subfolder in os.listdir(folderpath): # train, test, valid
        if subfolder == "test": continue # was causing problems
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
            if not os.path.exists(imagefilepath): 
                counter += 1
                errors.append(imagefilepath)
                continue
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
            shutil.copy(imagefilepath, f"{dest_path}/{subfolder}/images/{imagename}") # copy the image (only if it has labels)
    
    with open("data/various/errors.txt", "a") as f: print(errors, file = f)

def add_specific_dataset(dataset, dataset_classes, dest_folder = None, tot_classes = hardcoded_tot_classes):
    # now it works only bacause artichoke is already there, otherwise hardcoded classes have to be changed
    destination = dest_folder if dest_folder else "final"
    balance_count = {name:0 for name in tot_classes}
    # balance_count = find_dataset_balance(destination) # this is the proper way
    index_map = transform(dataset_classes, hardcoded_tot_classes)
    transfer_to_copy2(dataset, index_map, destination, balance_count)

def visualize_bboxes(imagepath, classes):
    labelmap = {index:value for index, value in enumerate(classes)}
    labelpath = imagepath.split("/")
    labelpath[-2] = "labels"
    labelpath[-1] = labelpath[-1][:-3] + "txt"
    labelpath = "/".join(labelpath)
    visualize_image_annotations(imagepath, labelpath, labelmap)

def fix_train_only():
    for folder in ["artichoke"]:
        os.makedirs(f"data/second_try/{folder}-1/valid/images", exist_ok=True)
        os.makedirs(f"data/second_try/{folder}-1/valid/labels", exist_ok=True)
        os.makedirs(f"data/second_try/{folder}-1/test/labels", exist_ok=True)
        os.makedirs(f"data/second_try/{folder}-1/test/images", exist_ok=True)
        folderpath = f"data/second_try/{folder}-1/train/images"
        names = os.listdir(folderpath)
        # print(folder, len(names))
        valid_len = len(names) // 100 * 20 # assign 20% of images to validation set
        test_len = len(names) // 100 * 10 # assign 10% of images to test set
        valid = random.choices(names, k = valid_len)
        test = random.choices(list(set(names).difference(set(valid))), k = test_len)
        # print(len(valid), len(test))
        # print(valid, test); exit()
        count_valid, count_test = 0, 0
        for imagefile in valid:
            labelfile = f"{imagefile[:-4]}.txt"
            imagepath = f"data/second_try/{folder}-1/train/images/{imagefile}"
            labelpath = f"data/second_try/{folder}-1/train/labels/{labelfile}"
            try:
                shutil.move(imagepath, f"data/second_try/{folder}-1/valid/images/{imagefile}")
                shutil.move(labelpath, f"data/second_try/{folder}-1/valid/labels/{labelfile}")
            except Exception as e:
                print(e, imagefile, labelfile, labelpath, imagepath, sep = "\n")
            count_valid += 1
        for imagefile in test:
            labelfile = f"{imagefile[:-4]}.txt" # i made an error here causing a lot of mess
            imagepath = f"data/second_try/{folder}-1/train/images/{imagefile}"
            labelpath = f"data/second_try/{folder}-1/train/labels/{labelfile}"
            try:
                shutil.move(imagepath, f"data/second_try/{folder}-1/test/images/{imagefile}")
                shutil.move(labelpath, f"data/second_try/{folder}-1/test/labels/{labelfile}")
            except Exception as e:
                print(e, imagefile, labelfile, labelpath, imagepath, sep = "\n")
            count_test += 1
        print(f"moved {count_valid} files to valid and {count_test} to test in folder {folder}")

def get_correspective_path(filepath: str) -> str:
    "get labels path from image path and viceversa"
    folder, extension = "images", "jpg"
    if filepath[-3:] == "jpg":
        folder, extension = "labels", "txt"
    temp_path = filepath.split("/")
    temp_path[-2] = folder
    temp_path[-1] = temp_path[-1][:-3] + extension
    return "/".join(temp_path)

def fix_test_labels_fucked_up(folder):
    "the problem is that the test images dont have a respective test label, they remained in the train ones"
    folderpath = f"data/second_try/{folder}/test/images"
    destfolder = f"data/second_try/{folder}/test/labels"
    counter = 0
    for imagefile in os.listdir(folderpath):
        labelfile = f"{imagefile[:-4]}.txt"
        imagepath = f"{folderpath}/{imagefile}"
        labelpath = f"data/second_try/{folder}/train/labels/{labelfile}"
        shutil.move(labelpath, f"{destfolder}/{labelfile}")
        counter += 1
    print(f"moved {counter} files for {folder}")

def find_dataset_balance(datafolder, classes = hardcoded_tot_classes):
    labelfolder = f"{datafolder}/labels"
    result = dict()
    mapping = {str(index) : value for index, value in enumerate(classes)}
    errors = []
    for labelfilename in os.listdir(labelfolder):
        labelfilepath = f"{labelfolder}/{labelfilename}"
        try:
            lines = open(labelfilepath, "r").readlines()
        except:
            errors.append(labelfilename)
            continue
        for line in lines:
            line = line.split(" ")
            first_int = line[0]
            result[mapping[first_int]] = result.get(mapping[first_int], 0) + 1
    print(errors, file = open(f"data/various/errors_in_balance.txt", "w"))
    balance = [(x,y) for x,y in result.items()]
    return sorted(balance, key = lambda x : -x[1])

def make_unique_dataset():
    destination = "merged2"
    # get dict of total classes to map indexes
    # to_add = {"initial-fruit-vegetables": ['banana_wb', 'banana', 'blackberry', 'raspberry', 'lemon_wb', 'lemon', 'grapes_wb', 'grapes', 'tomato_wb', 'tomato', 'apple_wb', 'apple', 'chilli_wb', 'chilli']} # i removed the wobs
    datasets = {k:v for k,v in get_datasets("data/second_try")}
    # datasets.update(to_add)
    tot_classes = get_classes(datasets) # = global tot classes
    print(tot_classes); exit()

    for dataset, labels in datasets.items():
        dataset_path = f"data/second_try/{dataset}"
        transfer_to_copy(dataset_path, labels, destination, tot_classes)

if __name__ == '__main__':

    # merge_everything(["test"])
    tempfolder = "data/second_try/initial-fruit-vegetables"
    folder = "bigger"
    print(find_dataset_balance(folder + "/train"))
    choice = random.choice(os.listdir(f"{folder}/train/images"))
    random_image1 = f"{folder}/train/images/" + choice
    visualize_bboxes(random_image1, hardcoded_tot_classes)
    # visualize_bboxes(random_image2, hardcoded_tot_classes)
    # print(label_to_label_map())
    # print(get_info(folderpath))
    # add_specific_dataset("data/second_try/artichoke-1", ["Artichoke"], "merged2", global_tot_classes)
