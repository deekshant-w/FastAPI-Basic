from fastapi import APIRouter, File, UploadFile
from wordcloud import WordCloud
import cv2
from starlette.responses import StreamingResponse
import io
from faker import Faker

fake = Faker()

router = APIRouter()

@router.get('/wordSummary')
async def wordSummary(text:str):
	data = text.split(' ')
	count = {}
	total = 0
	for word in data:
		count[word] = count.get(word,0) + 1
		total+=1
	payload = {
		'result' 		: count,
		'unique words'	: len(count),
		'total words'	: total
	}
	return payload

@router.get('/letterSummary')
async def letterSummary(text:str):
	count = {}
	for x in text:
		count[x] = count.get(x,0) + 1
	payload = {
		'result' 		: count,
		'unique keys'	: len(count),
		'total letters'	: len(text)
	}
	return payload

@router.get('/wordCloud')
async def wordCloud(text:str):
	wordcloud = WordCloud().generate(text).to_array()
	_, im_png = cv2.imencode(".png", wordcloud)
	bytesImage = im_png.tobytes()
	responce = StreamingResponse(io.BytesIO(bytesImage), media_type="image/png")
	return responce

@router.get('/fakeName/{count}')
def fakeName(count:int=1):
	result = [fake.name() for x in range(count)]
	return result

@router.get('/fakeAddress/{count}')
def fakeAddress(count:int=1):
	result = [fake.address() for x in range(count)]
	return result

@router.get('/fakeText/{count}')
def fakeText(count:int=1,sentences:int=5):
	result = [fake.paragraph(nb_sentences=sentences) for x in range(count)]
	return result

@router.get('/fakeProfile')
def fakeProfile():
	return fake.profile()

@router.get('/fakeTimeStamp/{count}')
def fakeTimeStamp(count:int=1):
	result = [fake.date_time() for x in range(count)]
	return result
