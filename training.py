from ultralytics import YOLO
import os, random, numpy as np

def test(model):
	'old function to test a model visually'
	folder = "merged2"
	params = {
		"name": "predict",
		"save": True,
		"project": "runs/detect/predict",
		"show": False,
		"classes": None, # quick way of choosing specific ids to predict among
		"conf": 0.1 # minimum level of confidence before showing a box
	}
	random_images = [f"{folder}/valid/images/" + random.choice(os.listdir(f"{folder}/valid/images")) for _ in range(10)]
	# model.predict("data/fridge_example.jpg", **params)
	model.predict("data/fridge_example2.jpg", **params)
	# model.predict("data/fridge_example3.jpg", **params)
	# model.predict("data/fruit_example.jpg", **params)
	results = model.predict([random_image for random_image in random_images], **params) # this should work as a good list
	# result have attribute boxes, contains the list of things found: https://docs.ultralytics.com/modes/predict/#working-with-results
	print(results)


best_model = YOLO("runs/detect/again_11m_bs16/weights/best.pt") # current best model that is imported from other files

# # Train the model
if __name__ == '__main__':

	# model = YOLO("models/default/yolo11m.pt") # COCO-pretrained YOLO model
	# results = model.train(data="data.yaml", epochs=30, imgsz=640, device=0) # how i initially trained
	# model = YOLO("runs/detect/train_small_bs16/weights/last.pt") # my model <- use last.pt to restore lr and optimizer state <- fake it didn't work
	model = best_model
	# model = YOLO(r"C:\Users\Pietro\Principale\Coding\Python\projects\siMagna\runs\detect\old\train_small_bs16\weights\best.pt")
	# model.info() # Display model information (optional)
	
	# the best batch size for 11s is 32, takes ~ 3mins per epoch but it could perform worse, to be tested
	# 16 workers seems a bit excessive
	# i should try batch = 0.8 or something -> use 80% of gpu memory
	# results = model.train(data = "again/data.yaml", epochs = 150, device = 0, batch = 16, name = "again_11m_bs16") # train
	# model.train(resume = True) # to resume from epoch 94 to 150
	# model.predict(r"C:\Users\Pietro\Downloads\How-to-save-money-on-groceries.webp", save = True)
	# model.predict(r"C:\Users\Pietro\Downloads\grocery-budget-tracking-6-of-12.jpg", save = True)
	tempfolder = "data/whatsapp/oug"
	# photos = ["C:/Users/Pietro/Downloads/predict/" + img for img in os.listdir("C:/Users/Pietro/Downloads/predict")]
	photos = [f"{tempfolder}/{img}" for img in os.listdir(tempfolder)]
	# photos = [r"data\Immagine WhatsApp 2025-07-01 ore 13.13.52_0f24702a.jpg", r"data\Immagine WhatsApp 2025-07-01 ore 13.13.52_30b50f4d.jpg"]
	model.predict(r"C:\Users\Pietro\Downloads\Main-scaled.jpg", save = True)
	model.predict(photos, save = True)

	# test(model)
	# print(get_ingredients(model, "data/egnaldphoto.jpg", conf = 0.1))
	# metrics = model.val(plots = True)
	