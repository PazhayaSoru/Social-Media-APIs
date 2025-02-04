from fastapi import HTTPException,status,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,schemas,oauth2


router = APIRouter(
  prefix='/vote',
  tags=['VOTE'],
)

#**function to vote on a post
@router.post("/",status_code=200,)
def vote(vote : schemas.Vote,user : dict = Depends(oauth2.get_current_user),db : Session = Depends(get_db)):

  vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,models.Vote.user_id == user.id)
  post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
  found_vote = vote_query.first()

  if not post:
    raise HTTPException(status_code=404,detail=f"Post with PostID: {vote.post_id} does not Exist")

  if vote.vote_dir == 1:
    if found_vote:
      raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"The User {user.username} has Already Liked The Post")
    
    created_vote = models.Vote(post_id=vote.post_id,user_id=user.id)
    db.add(created_vote)
    db.commit()
    return {"message":"added vote"}
  else:
    if not found_vote:
      raise HTTPException(status_code=404,detail="Vote does not Exist")
    vote_query.delete(synchronize_session=False)
    db.commit()
    return {"message":"Deleted Vote Successfully"}
      

