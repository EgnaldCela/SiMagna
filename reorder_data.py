import os
import shutil

sourcedir = "data/fruit for yolo/test/test"
imagesdir = "dataset/images/test"
labelsdir = "dataset/labels/test"

for element in os.listdir(sourcedir):
    # print(element, element[-3]); exit()
    if element[-3:] == "txt":
        shutil.move(f"{sourcedir}/{element}", f"{labelsdir}/{element}")
    elif element[-3:] == "jpg":
        shutil.move(f"{sourcedir}/{element}", f"{imagesdir}/{element}")
