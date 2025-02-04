from pydantic import BaseModel,EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional


#Schemas for Users
class UserBase(BaseModel):
  username : str
  email : EmailStr

class UserCreate(UserBase):
  password : str
  created_at : datetime

class User(UserBase):
  created_at : datetime
  class Config:
    from_attributes = True

class UserLogin(BaseModel):
  username : str
  password : str

class PostBase(BaseModel):
  title : str
  content : str
  published : bool = True


class PostCreate(PostBase):
  pass


class Post(PostBase):
  id: int
  #datetime helps us validate the date as well
  created_at : datetime
  user_id : int
  user : UserBase

class PostAlt(BaseModel):
  id : int
  title : str
  content : str
  published : bool = True
  created_at : datetime
  user_id : int


class PostwithVotes(BaseModel):
  Post : PostAlt
  votes : int

  #'Config' class enables to ORM Compatability (Pydantic-specific)
  class Config:
    #the from_attributes variable, when set to true, will tell pydantic to be ORM Compatable
    from_attributes = True



#schema for recieving the token from the client for verification
class Token(BaseModel):
  access_token : str
  token_type : str

class TokenData(BaseModel):
  id : Optional[str] = None

class Vote(BaseModel):
  post_id : int
  vote_dir : int # type: ignore





