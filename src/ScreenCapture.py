import ctypes
import os
import time
import cv2
from PIL import Image
import numpy as np
LibName = '../lib/screencapture.so'
AbsLibPath = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + LibName
grab = ctypes.CDLL(AbsLibPath)


def getScreenshot(x1, y1, x2, y2):
	start_time = time.time()
	w, h = x1 + x2, y1+y2
	size = w * h
	objLength = size * 3

	grab.getScreen.argtypes = []
	result = (ctypes.c_ubyte * objLength)()

	grab.getScreen(x1, y1, w, h, result)
	image = Image.frombuffer('RGB', (w, h), result, 'raw', 'RGB', 0, 1)
	image = np.array(image)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# cv2.imshow('Test', image)
	# print('{} seconds'.format(time.time() - start_time))
	# cv2.waitKey()
	# cv2.destroyAllWindows()
	print type(image)
	return image

def VideoAssembler():

	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	out = cv2.VideoWriter('output.avi',fourcc, 20.0, (1366,768))

	while(True):
	    
		frame = getScreenshot(0, 0, 1366, 768)
		# write the flipped frame
		out.write(frame)

		cv2.imshow('frame',frame)
	    
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		else:
			continue

	# Release everything if job is finished
	out.release()
	cv2.destroyAllWindows()
		


if __name__ == '__main__':
	VideoAssembler()