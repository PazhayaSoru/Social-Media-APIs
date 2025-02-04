from fastapi import FastAPI
from .routers import post,user,auth,votes
from fastapi.middleware.cors import CORSMiddleware
#This command instructs SQLAlchemy to create all the tables defined in the models module
# in the database connected to the engine. If the tables already exist, this operation won't create duplicates. (Not in Use)
#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#Set up for the CORS Middleware to enable domains that are listed int the 'origins' list to have access to our APIs
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



#ROOT function
@app.get("/")
def root():
  return {"message" : "hello world"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)





