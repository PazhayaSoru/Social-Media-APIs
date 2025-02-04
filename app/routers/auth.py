from fastapi import HTTPException,status,APIRouter,Depends
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models,schemas,utils,oauth2
from ..database import get_db



router = APIRouter(
  tags=["Authentication"],
  )

#function to let users login (with authentication)
@router.post("/login")
def login(user_credentials : OAuth2PasswordRequestForm = Depends(),db : Session = Depends(get_db)):
  pwd_entered = user_credentials.password
  #OAuth2PasswordRequestForm considers only two fields, username and password.
  user = db.query(models.User).filter(models.User.username == user_credentials.username).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'The User with Username: {user_credentials.username} does not exist')
  if not utils.verify_password(pwd_entered=pwd_entered,pwd_db=user.password):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Incorrect Credentials")
  
  access_token = oauth2.create_access_token(data={'user_id' : str(user.id),'username' : user.username})
  
  return {'token' : access_token, 'token_type':'bearer'}

    
