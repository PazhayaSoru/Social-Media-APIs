from typing import Optional,List
from fastapi import HTTPException,status,Depends,APIRouter
from sqlalchemy.orm import Session
#double dot implies that database is outside the current directory
from ..database import get_db
from .. import models,schemas,utils


router  = APIRouter(
  #stating that  all the path operations' URLs start with the prefix
  prefix="/users",
  #to seggregate APIs under a certain Tag/Category
  tags=['Users']

  )

#****Path Operations for Users****


#**function to create a user and register in Database**
@router.post("/",response_model=schemas.User,status_code=status.HTTP_201_CREATED)
def create_user(user:schemas.UserCreate,db : Session = Depends(get_db)):
  #Hashing the passowrd using the Password Context imported from utils
  hashed_pwd = utils.password_hash(user.password)
  user.password = hashed_pwd
  new_user = models.User(**dict(user))
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return (new_user)


#**function to get all the Users**
@router.get("/",response_model=List[schemas.User],status_code=status.HTTP_200_OK)
def get_users(db : Session = Depends(get_db)):
  users = db.query(models.User).all()
  if users == None:
    raise HTTPException(status_code=404,detail=f"No Users Created Yet")
  return users


@router.get("/{user_id}",status_code=status.HTTP_200_OK,response_model=schemas.User)
def get_user(user_id : int,db : Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.id == id).first()
  if not user:
    raise HTTPException(status_code=404,detail=f"[ERROR] The User with UserID: {user_id} does not exist")
  return user

@router.delete("/{user_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id : int, db : Session = Depends(get_db)):
  user_query = db.query(models.User).filter(models.User.id == user_id)

  if not user_query.first():
    raise HTTPException(status_code=404, detail=f"[ERROR] The User with UserID: {user_id} does not exist")
  user = user_query.first()
  user_query.delete(synchronize_session=False)
  db.commit()
