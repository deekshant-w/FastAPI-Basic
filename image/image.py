from fastapi import APIRouter, File, UploadFile, HTTPException, Query
import cv2
from starlette.responses import StreamingResponse
import base64
import io
from scipy import ndimage
from typing_extensions import Literal
from .helper import *
import time

app = APIRouter()

def pprint(*data):
	data = [str(x) for x in data]
	data = "-*-".join(data)
	handle = open('log','a')
	handle.write(data)
	handle.write('\n')
	handle.close()

@app.post('/crop')
async def crop(*,
		image 	: 	UploadFile = File(...), 
		startx 	: 	int,
		starty 	: 	int,
		endx	:	int,	
		endy	:	int,	
		):
	start = time.time()
	content = await image.read()

	pprint('await',time.time()-start)
	start = time.time()
	
	npImage = readImage(content)
	
	pprint('decode',time.time()-start)
	start = time.time()
	
	if(np.shape):
		if(startx>=endx or starty>=endy):
			raise HTTPException(status_code=422, detail="Start (x,y) should be less than end (x,y) respectively.")
		else:
			newImage = npImage[starty:endy,startx:endx]
			bytesImage = returnImage(newImage)
	else:
		raise HTTPException(status_code=400, detail="No Image")

	pprint('crop',time.time()-start)
	start = time.time()

	headers = {
		'fileName'	: f"{image.filename.split('.')[0]}.png",
		'fileLength': str(len(bytesImage))
	}

	responce = StreamingResponse(io.BytesIO(bytesImage), media_type="image/png", headers=headers)
	
	pprint('resp',time.time()-start)
	start = time.time()
	
	return responce

@app.post('/rotate')
async def rotate(
		times 	: int = Query(...,ge=-3,le=3,description='Positive value to rotate clockwise and negative value to rotate anti-clockwise'),
		image 	: UploadFile = File(...),
	):
	angle = times * 90
	content = await image.read()
	npImage = readImage(content)
	if(np.shape):
		newImage = ndimage.rotate(npImage, angle)
		bytesImage = returnImage(newImage)
	else:
		raise HTTPException(status_code=400, detail="No Image")
	
	headers = {
		'fileName'	: f"{image.filename.split('.')[0]}.png",
		'fileLength': str(len(bytesImage))
	}

	responce = StreamingResponse(io.BytesIO(bytesImage), media_type="image/png", headers=headers)
	return responce

@app.post('/flip')
async def flip(
		direction 	: Literal['v','h','b'] = Query(...,description='v for vertical or h for horizontal or b for both flip'),
		image 		: UploadFile = File(...),
	):
	content = await image.read()
	npImage = readImage(content)
	
	if(direction=='v'):
		npImage = cv2.flip(npImage, 0)
	elif(direction=='h'):
		npImage = cv2.flip(npImage, 1)
	npImage = cv2.flip(npImage, -1)
	
	bytesImage = returnImage(npImage)
	headers = {
		'fileName'	: f"{image.filename.split('.')[0]}.png",
		'fileLength': str(len(bytesImage))
	}
	
	responce = StreamingResponse(io.BytesIO(bytesImage), media_type="image/png", headers=headers)
	return responce

@app.post('/shrink')
async def shrink(
		ratio : float = Query(...,gt=0,lt=100,description='% to shrink'),
		image : UploadFile = File(...),
	):
	content = await image.read()
	npImage = readImage(content)

	width = int(npImage.shape[1] * ratio / 100)
	height = int(npImage.shape[0] * ratio / 100)
	dim = (width, height)

	resized = cv2.resize(npImage, dim, interpolation = cv2.INTER_AREA)
	bytesImage = returnImage(resized)
	
	headers = {
		'fileName'	: f"{image.filename.split('.')[0]}.png",
		'fileLength': str(len(bytesImage))
	}
	
	responce = StreamingResponse(io.BytesIO(bytesImage), media_type="image/png", headers=headers)
	return responce

@app.post('/bwimage')
async def bwimage(
		image : UploadFile = File(...),
	):
	content = await image.read()
	npImage = readImage(content)
	
	backtorgb = cv2.cvtColor(npImage, cv2.COLOR_BGR2GRAY)
	bytesImage = returnImage(backtorgb)

	headers = {
		'fileName'	: f"{image.filename.split('.')[0]}.png",
		'fileLength': str(len(bytesImage))
	}
	
	responce = StreamingResponse(io.BytesIO(bytesImage), media_type="image/png", headers=headers)
	return responce
