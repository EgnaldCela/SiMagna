from ultralytics import YOLO

# # Train the model
if __name__ == '__main__':
    # Load a COCO-pretrained YOLO model
	model = YOLO("yolo11n.pt")

	# Display model information (optional)
	model.info()  
	
	# results = model.train(data="data.yaml", epochs=30, imgsz=640, device=0) # how i initially trained
	
	# check how long the nano model takes to train
	# model.model.names.update({71: 'sink', 72: 'refrigerator', 73: 'book', 74: 'Rotor', 75: 'vase', 76: 'scissors'}) # update names without training again
	
	# inferencemodel = YOLO("runs/detect/train-11n/weights/best.pt") # i think it's the same as best.pt
	# result = inferencemodel("data/egnaldphoto.jpg", save = True) # run inference on a particular image and save the result

	# now let's try to train on the complete dataset
    # results = model.train(data="dataset_merge_test/data.yaml", epochs=60, imgsz=640, device=0) # wonderful, i fucked up with the labels
    