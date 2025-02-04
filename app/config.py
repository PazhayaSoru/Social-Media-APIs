from pydantic_settings import BaseSettings


#This class extracts the variables in the env file and
class Settings(BaseSettings):
  database_hostname : str
  database_password : str
  database_name : str
  database_username : str
  secret_key : str
  algorithm : str
  token_expire_minutes : int
  
  # We are telling pydantic that the env variables are stored in the file named '.env' 
  class Config:
    env_file = ".env" 



settings = Settings()