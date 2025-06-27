from ultralytics import YOLO
import os, random

def test(model):
	folder = "merged2"
	random_images = [f"{folder}/valid/images/" + random.choice(os.listdir(f"{folder}/valid/images")) for _ in range(10)]
	model("data/fridge_example.jpg", save = True)
	model("data/fridge_example2.jpg", save = True)
	model("data/fridge_example3.jpg", save = True)
	model("data/fruit_example.jpg", save = True)
	[model(random_image, save = True) for random_image in random_images]

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

	# model = YOLO("yolo11m.pt") # COCO-pretrained YOLO model
	model = YOLO("runs/detect/train4/weights/best.pt") # my model
	
	# model.info() # Display model information (optional)
	 
	# results = model.train(data = "merged2/data.yaml", epochs = 1, imgsz = 640, device = 0) # train
	test(model)
	