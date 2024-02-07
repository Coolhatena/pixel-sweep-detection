import cv2
import json
import numpy as np

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

image = cv2.imread("img_1.jpg")



filter_thr = len(filters)
filter_count = 0
# cv2.rectangle(image, (roi["x"], roi["y"]), (roi["x"] + roi["width"], roi["y"] + roi["height"]), (0, 255, 00), 1, cv2.LINE_4)
filter = filters[filter_count]
croppped_image = image[roi["y"]:(roi["y"] + roi["height"]), roi["x"]:(roi["x"] + roi["width"])].copy()
hsv = cv2.cvtColor(croppped_image, cv2.COLOR_BGR2HSV)
MASK_DOWN = np.array(filter["DOWN"])
MASK_UP = np.array(filter["UP"])
msk = cv2.inRange(hsv, MASK_DOWN, MASK_UP)

is_correctly_ordered = False

for i in range(0, len(msk)):
	for j in range(0, len(msk[i])):
		if msk[i][j] == 255:
			filter_count += 1
			if filter_count < filter_thr:
				# msk[i][j] = 150
				# print(filter_count)
				filter = filters[filter_count]
				msk = updateFilteredImg(hsv, filter)
				cv2.imshow(f"Imagen {filter_count}", msk)
			else:
				is_correctly_ordered = True


print(is_correctly_ordered)
print(filter["COLOR"])
cv2.imshow("Imagen", msk)
cv2.waitKey(0)