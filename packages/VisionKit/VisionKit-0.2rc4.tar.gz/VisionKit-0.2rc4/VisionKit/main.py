""" Main interface for VisionKit """

# For using VisionKit.kits.KitName
import .kits as kits

# For using VisionKit.opencv
import cv2 as opencv

if __name__ == "__main__":
	print("Running as a script")
	print("Starting tests")
	
	# Test greentape
	greenfind = kits.PresetKit()
	greenfind.setPipeline("greentape")
	greenfind.setCam(0)
	print(greenfind.getData())
	greenfind.closeCam()
	
	# RaiderShirtFind
	rsf = kits.PresetKit()
	rsf.setPipeline("raidershirtfind")
	rsf.setCam(0)
	print(rsf.getData())
	rsf.closeCam()