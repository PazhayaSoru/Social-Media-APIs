from passlib.context import CryptContext

#Creating a Password Context wherein, we are using the bcrypt algorithm to hash the password. If the scheme/algorithm 
#is no longer considered secure, then passlib will automatically mark it as deprecated and warn us when used.
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")


def password_hash(password : str):
  return pwd_context.hash(password)

def verify_password(pwd_entered : str, pwd_db : str):
  return pwd_context.verify(pwd_entered,pwd_db)