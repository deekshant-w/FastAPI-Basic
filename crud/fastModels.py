from pydantic import BaseModel, EmailStr
from typing import List, Optional

Database = [
	{
		'name':'Deekshant Wadhwa',
		'email':'deekshantwadhwa2000@gmail.com',
		'val':7,
		'text':'I am the creator!',
	},
	{
		'name':'Vadee',
		'val':238,
		'text':'~ I was, I am and I always will ~',
		'contactme':True,
	},
]


class User(BaseModel):
	name 	: str 
	email 	: Optional[EmailStr] 	= 'user@anonymous.com'
	val 	: float 				= 1.0
	text 	: Optional[str] 		= 'Howdy!!'
	contactme: bool 				= False

class Update(BaseModel):
	name 	: Optional[str] 
	email 	: Optional[EmailStr]
	val 	: Optional[float]
	text 	: Optional[str]
	contactme: Optional[bool]