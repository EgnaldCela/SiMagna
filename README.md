# siMagna!

### Where are we now
* I put together a dataset that kinda works, the classes used are in the end of temp.ipynb, where the value is the number of bounding boxes for each label
* some things like artichoke are not part of it because it wasn't working
* a problem could be unbalanced classes, as you can see from the table in temp -^
* another problem is that there are some segments among the boxes, they should be found and removed
* trained 11m for 1 epoch, it takes around 8 minutes, weights are in runs/detect/train/weights
* also trained a better 11s for 72 epochs, weights are in runs/detect/from_scratch_bs32/weights
* you should start working on the interface, just assume you have a list of ingredients found as i wrote there
* I also think it would be nice to add ingredients, so check if you find something
* let's try to not interfere with each others github changes, for example i will not touch the interface

### Pipeline
1. Prepare dataset based on the recipes
    * starting point of ingredients: "groceries.csv"
    * ingredients ordered by frequency (i hope): "sorted_ingredients_test.csv"
2. Object detection → YoloV11, size n, s or m
3. Get categories → still have to find how <- i found it and i didnt take a note anywhere
4. Graphical interface → gradio 

### Structure - needed functions
- [] way to take an input: (user input) -> (image)
- [] maybe preprocessing: (image) -> (image)
- [] object detection: (image) -> (image with labelled boxes, list of ingredients)
- [] give the output to the recipe finder: (list of ingredients) -> (list of recipes)

### Datasets - useless basically
| name | links | used | description |
|:-------------:|:----------------:|:----------------------:|:------:|
| initial one with fruit with or w/o bags | [kaggle]() | only one used | everything on the same background |
| fruit and vegetables image recognition | [kaggle](https://www.kaggle.com/datasets/kritikseth/fruit-and-vegetable-image-recognition) | not used | 36 categories! |
| grocery1 | [roboflow](https://universe.roboflow.com/dmitri-kaslov-fmitx/grocery1/dataset/1) | downloaded! | very noisy and augmented, in different places like supermarket |
| food detection 5 (?) | [roboflow](https://universe.roboflow.com/scan-detection/food-detection-hipfv/dataset/5) | i downloaded the first (9k pics) | plain single objects |
| pathpal grocery detector (multiple versions) | [roboflow](https://universe.roboflow.com/grocery-pathpal-sahaay/pathpal-grocery-detector-3/dataset/10) | downloaded 3-2 and 3-10 | |
| foodtypes individual... | [roboflow](https://universe.roboflow.com/tk-matima-unqyz/foodtypes-individual-in-fridge/dataset/1#) | downloaded | seems a smaller version of grocery1 |
| food item detection 15k | [roboflow](https://universe.roboflow.com/coretus/food-item-detection-fggyf/dataset/1) | downloaded | many images and also fridge env, a lot of noise |
| random one found on github for v8 | [github](https://github.com/anushkaspatil/Food-Detection) | not downloaded |
| nuts, almonds and more... | [google](https://datasetsearch.research.google.com/search?src=0&query=object%20recognition%20nuts&docid=L2cvMTF4N2g1aHI0Mw%3D%3D) | ... |
| just nuts | [google](https://datasetsearch.research.google.com/search?src=0&query=object%20recognition%20nuts&docid=L2cvMTF4N3JyZ3ZmcA%3D%3D) | - [ ] |
| soybean | [google](https://datasetsearch.research.google.com/search?src=0&query=object%20recognition%20seeds&docid=L2cvMTFtNjhqbDhtYg%3D%3D) | - [ ] |
| meat detection, chicken | [google](https://datasetsearch.research.google.com/search?src=0&query=object%20recognition%20meat&docid=L2cvMTF4MmtxYmc2aA%3D%3D) | - [ ] |
| meat detection, ingredients | [google](https://datasetsearch.research.google.com/search?src=0&query=object%20recognition%20meat&docid=L2cvMTF4N3pzMDBiYg%3D%3D) | - [ ] |
| mygroceyproducts, similar | [roboglow](https://universe.roboflow.com/dmitri-kaslov-fmitx/mygroceryproducts/dataset/1) | it's for CNN :( |

### Useful stuff
* train yolov4 on roboflow [video](https://www.youtube.com/watch?v=9hVgyeI4g4o)
* 1h yolo11 [video](https://www.youtube.com/watch?v=etjkjZoG2F0&authuser=0&themeRefresh=1&sttick=0)