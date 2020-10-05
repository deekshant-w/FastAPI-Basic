import numpy as np
import cv2

def debugImg(img):
	"""
	Display image for debugging
	Arguments:
		img : np array (image)
	"""
	cv2.imshow('image',img)
	cv2.waitKey()

def readImage(byteImage):
	"""
	Convert byte array image to
	numpy array
	Arguments:
		byteImage 	: Image in byte format
	Returns:
		Image as numpy array
	"""
	nparr = np.fromstring(byteImage, np.uint8)
	img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
	return img

def returnImage(npImage):
	"""
	Convert numpy array image to
	byte image
	Arguments:
		npImage	: Numpy array ie. Image
	Return:
		bytesImage : image as png bytes
	"""
	_, im_png = cv2.imencode(".png", npImage)
	bytesImage = im_png.tobytes()
	return bytesImage