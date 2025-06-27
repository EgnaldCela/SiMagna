from ultralytics import YOLO
import os, random

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
	# random_images = [f"{folder}/valid/images/" + random.choice(os.listdir(f"{folder}/valid/images")) for _ in range(10)]
	# model.predict("data/fridge_example.jpg", **params)
	model.predict("data/fridge_example2.jpg", **params)
	# model.predict("data/fridge_example3.jpg", **params)
	# model.predict("data/fruit_example.jpg", **params)
	# [model.predict(random_image, **params) for random_image in random_images]
	# result have attribute boxes, contains the list of things found: https://docs.ultralytics.com/modes/predict/#working-with-results

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

	# model = YOLO("yolo11s.pt") # COCO-pretrained YOLO model
	# model = YOLO("runs/detect/train_small_bs16/weights/last.pt") # my model <- use last.pt to restore lr and optimizer state <- fake it didn't work
	model = YOLO("runs/detect/from_scratch_bs32/weights/best.pt")
	# model.info() # Display model information (optional)
	
	# the best batch size for 11s is 32, takes ~ 3mins per epoch but it could perform worse, to be tested
	# 16 workers seems a bit excessive
	# results = model.train(data = "merged2/data.yaml", epochs = 150, resume = False, imgsz = 640, device = 0, cache = False, batch = 32, name = "from_scratch_bs32") # train
	# results = model.train(data = "merged2/data.yaml", epochs = 150, resume = True, save_period = 10, imgsz = 640, device = 0, batch = 16, name = "continue_small_bs16") # didn't work
	# i should try batch = 0.8 or something -> use 80% of gpu memory
	# model.train(resume = True) # to resume from epoch 73 to 150

	# test(model)
	metrics = model.val(plots = True)
	