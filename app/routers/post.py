from typing import Optional,List
from fastapi import HTTPException,status,Depends,APIRouter
from sqlalchemy.orm import Session
#double dot implies that database is outside the current directory
from ..database import get_db
from .. import models,schemas,oauth2
from sqlalchemy import func

router = APIRouter(
  #stating that  all the path operations' URLs start with the prefix
  prefix='/posts',
  #to seggregate APIs under a certain Tag/Category
  tags=['Posts']
  )

#**function for getting all the posts (entries) in the database**
#the response model utilises 'List' from typing module to send 
#data that is in the form of a list
@router.get("/",response_model=List[schemas.PostwithVotes])
def get_posts(db : Session = Depends(get_db),limit : int = 10,skip : int  = 0,search: Optional[str] = ""):
  #getting all the entries using SQLAlchemy query
 
  posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
  models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).offset(skip).limit(limit).all()

  return (posts)

#**function for getting a post with the specified ID**
@router.get("/{post_id}",response_model=schemas.PostwithVotes)
def get_post(post_id : int,db:Session = Depends(get_db),user : dict = Depends(oauth2.get_current_user)):
  #this query is going to fetch the first instance that matches the condition given for filtering
  post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
  models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == post_id).first()

  return(post)


# **function for registering a new entry into the database**
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post : schemas.PostCreate,db : Session = Depends(get_db),user : dict = Depends(oauth2.get_current_user)):
  #the 'dict(post)' is used to structure the post object into a dictionary and the '**'
  #preceding it will unpack all the entries so that we can fill in the details for creating a 'Post' object
  post_dict = dict(post)
  post_dict['user_id'] = user.id
  new_post = models.Post(**post_dict)
  #adding the entry into the Database
  db.add(new_post)
  #commiting the changes
  db.commit()
  db.refresh(new_post)
  return new_post

#**function to delete an entry (Post)**
@router.delete("/{post_id}",status_code=status.HTTP_200_OK,response_model=schemas.Post)
def delete_posts(post_id : int,db : Session = Depends(get_db),user : dict = Depends(oauth2.get_current_user)):
  post_query = db.query(models.Post).filter(models.Post.id == post_id)

  # we first check if an entry with a particular ID exists. If not ,we handle the exception 
  post = post_query.first()
  if post_query.first() == None:
    raise HTTPException(status_code=404,detail=f'[ERROR] The Post with PostID: {post_id} does not exist')
  
  #Checking whether the post belongs to the logged in user
  if post.user_id != user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
  
  #if it does exist, then we delete it
  post_query.delete(synchronize_session=False)
  db.commit()
  return post_query
  

#**function for updating a particular entry**
@router.put("/{post_id}",response_model=schemas.Post,)
def update_post(post_id:int,post:schemas.PostCreate,db : Session = Depends(get_db),user: dict = Depends(oauth2.get_current_user)):
  post_query = db.query(models.Post).filter(models.Post.id == post_id)
  retrieved_post = post_query.first()
  if retrieved_post == None:
    raise HTTPException(status_code=404,detail=f"[ERROR] The Post with PostID: {post_id} does not exist")
    
  if retrieved_post.user_id != user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")

  post_dict = dict(post)
  post_dict['id'] = retrieved_post.id 
  post_dict['created_at'] = retrieved_post.created_at
  post_dict['user_id'] = retrieved_post.user_id

  post_query.update(post_dict,synchronize_session=False)
  db.commit()
  return retrieved_post
