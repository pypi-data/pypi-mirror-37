""" Define various avalible kits"""
import cv2

# Import various presets
from kitfiles import greentape as greentape
from kitfiles import raidershirtfind as rsf

avalible_presets = {
	"greentape" : greentape.GreenTape(),
	"raidershirtfind" : rsf.RaiderShirtFind()
}

## PresetKit ##
class PresetKit(object):
	""" Uses GRIP Pipelines to do simple vision tasks """
	def __init__(self, logging: bool = True) -> None:
		self.logging_enabled = logging
		self.camera = 0
		self.pipeline = None
	
	def setCam(self, cam_id: int) -> None:
		self.__LOG("Creating CV2 camera")
		self.camera = cv2.VideoCapture(cam_id)
	
	def getData(self) -> dict:
		""" Use a preset pipeline to get data about the image """
		# Get a frame from opencv
		new_frame, frame = self.camera.read()
		
		if new_frame:
			# Process the frame
			self.pipeline.process(frame)
			# Construct a dict
			output = {"success": False, "x":[], "y":[], "h":[], "w":[]}
			
			# iterate through frames
			for processed_frame in self.pipeline.filter_contours_output:
				# Use opencv's rects to get dimensions
				x, y, w, h = cv2.boundingRect(processed_frame)
				
				# Append data to output dict
				output["x"].append(x + w / 2)
				output["y"].append(y + h / 2)
				output["h"].append(w)
				output["w"].append(h)
			
			
			output["success"] = True
			return output
		else:
			return {"success": False}
	
	def setPipeline(self, name: str) -> None:
		if name in avalible_presets:
			self.pipeline = avalible_presets[name]
		else:
			print(name + " is not an avalible pipeline")
	
	def __LOG(self, text: str) -> None:
		""" Optional logging to stdout """
		if self.logging_enabled:
			print(text)

## CustomKit ##
