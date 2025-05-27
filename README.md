# siMagna!

### Pipeline
1. Object detection → YoloV11m
2. Recipe suggestions → API for online big model, pre existing
3. Graphical interface → gradio. (others to be explored) made by us 

### Datasets
| description | links | used | description |
|:-------------:|:----------------:|:----------------------:|:------:|
| initial one with fruit with or w/o bags | [kaggle]() | only one used | everything on the same background |
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