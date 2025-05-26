from ultralytics import YOLO

# Load a COCO-pretrained YOLO model
model = YOLO("yolo11m.pt")

# Display model information (optional)
model.info()

# # Train the model
if __name__ == '__main__':
	# results = model.train(data="data.yaml", epochs=30, imgsz=640, device=0) # how i initially trained
	inferencemodel = YOLO("runs/detect/train6/weights/last.pt") # i think it's the same as best.pt
	result = inferencemodel("data/egnaldphoto.jpg", save = True) # run inference on a particular image and save the result

# # Run inference with the YOLOv8n model on the 'bus.jpg' image
# results = model("path/to/bus.jpg")