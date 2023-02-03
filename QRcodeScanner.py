import cv2
import numpy as np
from matplotlib import pyplot as plt

def boxSize(arr):
	global data
	box_roll = np.rollaxis(arr,1,0)	  # 轉置矩陣，把 x 放在同一欄，y 放在同一欄
	xmax = int(np.amax(box_roll[0]))  # 取出 x 最大值
	xmin = int(np.amin(box_roll[0]))  # 取出 x 最小值
	ymax = int(np.amax(box_roll[1]))  # 取出 y 最大值
	ymin = int(np.amin(box_roll[1]))  # 取出 y 最小值
	return (xmin,ymin,xmax,ymax)

cap = cv2.VideoCapture("4K_QRcode_60to100.mp4")

while True:
	_, img = cap.read()
	#img = cv2.resize(img,(540,960))
	img = cv2.flip(img, 0)
	img = cv2.flip(img, 180)

	img1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	#ret, output1 = cv2.threshold(img1, 20, 255, cv2.THRESH_BINARY)
	output1 = cv2.adaptiveThreshold(img1, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 25, 30)
	height, width = output1.shape[:2]
	
	tmp = 500
	y1 = 0
	y2 = tmp
	x1 = 0
	x2 = tmp

	qrcode = cv2.QRCodeDetector()
	
	for i in range(2, 10):
		y1 = 0
		y2 = tmp
		for j in range(2, 10):
			crop_img = output1[int(y1):int(y2), int(x1):int(x2)]
			
			data, bbox, rectified = qrcode.detectAndDecode(crop_img)  # 偵測圖片中的 QRCode
			if bbox is not None:
				#print(data)
				#print(bbox)
				#print(rectified)
				box = boxSize(bbox[0])
				cv2.rectangle(output1[y1:y2, x1:x2],(box[0],box[1]),(box[2],box[3]),(0,0,255),7)  # 畫矩形
				cv2.rectangle(img[y1:y2, x1:x2],(box[0],box[1]),(box[2],box[3]),(0,0,255),7)  # 畫矩形
				cv2.namedWindow("Frame2", 0)
				cv2.resizeWindow("Frame2", 640, 480)
				cv2.imshow("Frame2", output1[y1:y2, x1:x2])

			
			y1 = y2 + 1
			y2 = tmp * j
			if(y1 >= 3840):
				break
			
		x1 = x2 + 1
		x2 = tmp * i
		if(x1 >= 2160):
				break
	
	cv2.namedWindow("Frame", 0)
	cv2.resizeWindow("Frame", 540, 960)
	cv2.imshow("Frame", output1)
	
	key = cv2.waitKey(1)
	if key == 60:
		break
		
cap.release()
cv2.destroyAllWindows()