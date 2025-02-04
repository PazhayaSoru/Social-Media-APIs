from jose import jwt, JWTError
from datetime import datetime,timedelta,timezone
from . import schemas,database,models
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException,Depends,status
from sqlalchemy.orm import Session
from .config import settings
#we need to provide a secret key (it could be any string)
#we also need to specify the algorithm that is used for enryption
#We need to specify the Expiration Time as well


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.token_expire_minutes

def create_access_token(data : dict):
  data_to_encode = data.copy()
  expiration_date = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES);
  data_to_encode['exp'] = expiration_date;
  encoded_jwt = jwt.encode(data_to_encode,SECRET_KEY,algorithm=ALGORITHM)
  return encoded_jwt

def verify_access_token(token : str, credentials_exception):
  
  try:
    print(token)
    decoded_data = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    user_id: str = decoded_data.get('user_id')

    if user_id is None:
      raise credentials_exception
    #make sure that you pass in a string in the schema
    token_data = schemas.TokenData(id=user_id)
  except JWTError:
    raise credentials_exception
  return token_data


def get_current_user(token : str = Depends(oauth2_scheme),db : Session = Depends(database.get_db)):
  credentials_exception = HTTPException(status_code=401,detail="Could not validate credentials",headers={'WWW-Authenticate':"Bearer"})

  token = verify_access_token(token,credentials_exception)
  id = token.id
  user = db.query(models.User).filter(models.User.id == id).first()

  return user

  
