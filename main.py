from ultralytics import YOLO
import os, random

# # Train the model
if __name__ == '__main__':
    # Load a COCO-pretrained YOLO model
	model = YOLO("runs/detect/train-11n-35epochs/weights/best.pt")

	# Display model information (optional)
	model.info()  
	
	# results = model.train(data="data.yaml", epochs=30, imgsz=640, device=0) # how i initially trained
	
	# check how long the nano model takes to train -> around 6min per epoch
	# model.model.names.update({71: 'sink', 72: 'refrigerator', 73: 'book', 74: 'Rotor', 75: 'vase', 76: 'scissors'}) # update names without training again
	
	# inferencemodel = YOLO("runs/detect/train-11n/weights/best.pt") # i think it's the same as best.pt
	# result = inferencemodel("data/egnaldphoto.jpg", save = True) # run inference on a particular image and save the result

	# now let's try to train on the complete dataset
    # results = model.train(data="merged_dataset/data.yaml", epochs=60, imgsz=640, device=0) # wonderful, i fucked up with the labels
	# results = model.train(data="merged_dataset/data.yaml", epochs=30, imgsz=640, device=0, name="train-11n-35epochs") # train!

	# random_images = ["merged_dataset/valid/images/" + random.choice(os.listdir(f"merged_dataset/valid/images")) for _ in range(10)]
	# model("data/egnaldphoto.jpg", save = True)
	# model("data/fridge_example.jpg", save = True)
	# model("data/fridge_example2.jpg", save = True)
	model("data/fridge_example3.jpg", save = True)
	# model("data/fruit_example.jpg", save = True)
	# [model(random_image, save = True) for random_image in random_images]