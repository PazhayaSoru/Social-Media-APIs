from .database import Base
from sqlalchemy import Column,Integer,String,Boolean,TIMESTAMP,text,ForeignKey
from sqlalchemy.orm import relationship


#implementation of SQLAlchemy Model for Posts
class Post(Base):
  #name of the table that is to be set and created in the database
  __tablename__="posts"

  id =  Column(Integer,primary_key=True,nullable=False)
  title = Column(String,nullable=False)
  content = Column(String,nullable=False)
  published = Column(Boolean,server_default='True',nullable=False)
  #'server_default' is the default value that is to be set for this particular attribute in the database. 
  #We can either pass in the value itself or indirectly set it using a SQL function
  created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('NOW()'))
  user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)

  user = relationship("User")
  

class User(Base):
  __tablename__ = "users"
  id = Column(Integer,nullable=False,primary_key=True)
  username = Column(String,nullable=False,unique=True)
  email = Column(String,nullable=False,unique=True)
  password = Column(String,nullable=False)
  created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('NOW()'))


class Vote(Base):
  __tablename__="votes"
  
  post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),nullable=False,primary_key=True)
  user_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),nullable=False,primary_key=True)