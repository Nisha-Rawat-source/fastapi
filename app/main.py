from typing import Optional
from fastapi import FastAPI, Response,status,HTTPException
from fastapi import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

my_post = [{"title":"my fav places" , "content":"my post no1 ","id":1},
           {"title":"my fav food" , "content":"my fav food is rice ","id":2}]

def findIndex(id):
    for i, p in enumerate(my_post):# here bhot i(index) and p(element) is in enumerate, enumerate(my_post), it gives both the index and the element
         if p['id'] == id:
            return i

def findPost(id):
    for p in my_post:
        if p['id'] == id:
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
#status_code=status.HTTP_201_CREATED is changing the status for path operation
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post: post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,1000000)
    my_post.append(post_dict)
    return {"data": post}


#giving the post with the entred id
@app.get("/posts/{id}")#path parameter
def get_post(id: int, response: Response):
    post = findPost(id)

    #we are chaning status code here for a specific condition
    if not post:
        #response.status_code = 404 one way to do it
        #response.status_code = status.HTTP_404_NOT_FOUND#another way to change the http response
        #return {"message": f"post with id: {id} does not found"}
        # can do it in more better way upar we were changing response however we can also use build in exception here
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not found")
    return{"post details":post}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    index = findIndex(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} does not exist")
    
    my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: post):

    index = findIndex(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} does not exist")
    
    mypostDict = post.model_dump()
    mypostDict['id'] = id
    my_post[index] = mypostDict

    return {"data": mypostDict}
    