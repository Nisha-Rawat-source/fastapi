from typing import Optional
from fastapi import FastAPI, Response
from fastapi import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

my_post = [{"title":"my fav places" , "content":"my post no1 ","id":1},
           {"title":"my fav food" , "content":"my fav food is rice ","id":2}]

def findPost(id):
    for p in my_post:
        if p["id"] == id:
            return p
        

#given is a pydantic model it defines the way we will get data from ui (postman)
#A Pydantic model defines the structure and validation(check) rules for request data sent by a client
class post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

#this the path function
@app.get("/")
def root():
    return {"message":"hello world"}


#this is the path fuction which is giving all the post available
@app.get("/posts")
def get_posts():
    return {"message":my_post}


#creating the post in the array 
@app.post("/posts")
def create_post(post: post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,1000000)
    my_post.append(post_dict)
    return {"data": post}


#giving the post with the entred id
@app.get("/posts/{id}")#path parameter
def get_post(id: int, response: Response):
    post = findPost(id)
    if not post:
        response.status_code = 404
    return{"post details":post}