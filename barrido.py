import cv2
import json
import numpy as np
import time

WINDOW_NAME = "Deteccion"

# cap = cv2.VideoCapture(0)

# while not cap.isOpened():
# 	print("Searching for camera")
# 	time.sleep(.5)
# 	cap = cv2.VideoCapture(0)

def updateFilteredImg(img, filter):
    MASK_DOWN = np.array(filter["DOWN"])
    MASK_UP = np.array(filter["UP"])
    msk = cv2.inRange(hsv, MASK_DOWN, MASK_UP)

    return msk

# Open JSON config file to get configuration data
with open('config.json', 'r') as config_file:
    json_raw_data = config_file.read()
    
json_data = json.loads(json_raw_data)

roi_data = json_data["roi_data"]
roi = roi_data[0]
print(roi_data)

filters = json_data["filters"]

image = cv2.imread("img_8.jpg")

while True:
	# cap = cv2.VideoCapture(0)
	while True:
		image = cv2.imread("img_8.jpg")
		# ret, image = cap.read()
		cv2.imshow(WINDOW_NAME, image)
		key = cv2.waitKey(1)
		if key == ord("b"):
			print('START...')
			break

		if key == ord("q"):
			print('END')
			cv2.destroyAllWindows()
			exit()


	cv2.rectangle(image, (roi["x"], roi["y"]), (roi["x"] + roi["width"], roi["y"] + roi["height"]), (0, 255, 00), 1, cv2.LINE_4)
	# Create sub roi's based on parameters
	croppped_images = []
	for roi_position in roi["subroi"]:
		cv2.rectangle(image, (roi_position, roi["y"]), (roi_position + roi["subroi_width"], roi["y"] + roi["height"]), (0, 255, 00), 1, cv2.LINE_4)
		croppped_images.append(image[roi["y"]:(roi["y"] + roi["height"]), roi_position:(roi_position + roi["subroi_width"])].copy())

	# iterator = 0
	# for roi_img in croppped_images:
	# 	cv2.imshow(f"Imagen_{iterator}", roi_img)
	# 	iterator += 1
	filter_thr = len(filters)
	filter_count = 1
	filter = filters[0]

	for roi_img in croppped_images:

		# croppped_image = image[roi["y"]:(roi["y"] + roi["height"]), roi["x"]:(roi["x"] + roi["width"])].copy()
		hsv = cv2.cvtColor(roi_img, cv2.COLOR_BGR2HSV)
		MASK_DOWN = np.array(filter["DOWN"])
		MASK_UP = np.array(filter["UP"])
		msk = cv2.inRange(hsv, MASK_DOWN, MASK_UP)

		is_correctly_ordered = False
		pixel_count = 0
		for i in range(0, len(msk)):
			for j in range(0, len(msk[i])):
				if msk[i][j] == 255:
					pixel_count += 1
					if pixel_count >= 20:
						pixel_count = 0
						#print(f'{filter["COLOR"]}: {(j, i)}')
						if filter_count <= filter_thr:
							# print(filter_count)
							msk[i][j] = 140
							image[i + roi["y"]][j + roi["x"]] = (0, 255, 0)
							# msk[i][j] = 150
							# print(filter_count)
							if filter_count < filter_thr:
								filter = filters[filter_count]
								msk = updateFilteredImg(hsv, filter)
							#cv2.imshow(f"Imagen {filter_count}", msk)
						else:
							is_correctly_ordered = True
						filter_count += 1


	print(is_correctly_ordered)
	print(filter["COLOR"])
	print(msk.shape)
					
	cv2.imshow("Imagen", msk)
	cv2.imshow("ROI", cv2.resize(image, (1040,480)))
	cv2.waitKey(0)
	cv2.destroyAllWindows()
