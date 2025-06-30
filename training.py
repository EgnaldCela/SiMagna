from ultralytics import YOLO
import os, random, numpy as np

def test(model):
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

def get_ingredients(model: YOLO, image: str | np.ndarray, conf: float | None = None) -> list[str]:
	results = model.predict(image, save = True, conf = conf) # it should work with all formats
	result = results[0] # result[0] because we feed a single image
	ingredient_IDs = result.boxes.cls.tolist()
	names = result.names
	food_found = [names[id] for id in ingredient_IDs]
	return food_found


def old_stuff():
	# results = model.train(data="data.yaml", epochs=30, imgsz=640, device=0) # how i initially trained
	# check how long the nano model takes to train -> around 6min per epoch
	# model.model.names.update({71: 'sink', 72: 'refrigerator', 73: 'book', 74: 'Rotor', 75: 'vase', 76: 'scissors'}) # update names without training again
	
	# inferencemodel = YOLO("runs/detect/train-11n/weights/best.pt") # i think it's the same as best.pt
	# result = inferencemodel("data/egnaldphoto.jpg", save = True) # run inference on a particular image and save the result

	# now let's try to train on the complete dataset
    # results = model.train(data="merged_dataset/data.yaml", epochs=60, imgsz=640, device=0) # wonderful, i fucked up with the labels
	# results = model.train(data="merged_dataset/data.yaml", epochs=30, imgsz=640, device=0, name="train-11n-35epochs") # train!
	pass

# # Train the model
if __name__ == '__main__':

	model = YOLO("yolo11s.pt") # COCO-pretrained YOLO model
	# model = YOLO("runs/detect/train_small_bs16/weights/last.pt") # my model <- use last.pt to restore lr and optimizer state <- fake it didn't work
	# model = YOLO("runs/detect/from_scratch_bs32/weights/best.pt")
	# model.info() # Display model information (optional)
	
	# the best batch size for 11s is 32, takes ~ 3mins per epoch but it could perform worse, to be tested
	# 16 workers seems a bit excessive
	# i should try batch = 0.8 or something -> use 80% of gpu memory
	results = model.train(data = "final/data.yaml", epochs = 150, resume = False, imgsz = 640, device = 0, cache = False, batch = 32, name = "final_bs32") # train
	# model.train(resume = True) # to resume from epoch 94 to 150

	# test(model)
	print(get_ingredients(model, "data/egnaldphoto.jpg", conf = 0.1))
	# metrics = model.val(plots = True)
	