import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from MIRA_QA import MIRA
from training import train_mira
from mira_view import html_content, html_content_convo
from message import add_message
app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://ec2-3-106-224-103.ap-southeast-2.compute.amazonaws.com:8000",
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Question(BaseModel):
    question: str
    key:str


# endpoint for asking questions
@app.post('/api/mira/ask')
async def mira(ques:Question):
    mira = MIRA()
    # try:
    # verify the key
    if ques.key != os.getenv('MIRA_KEY'):
        return {"success":"false","msg":"Unauthorized"}
    
    #add_message(ques.question,"HUMAN",ques.conversation_id)
    # retrieve the similar chunks
    docs = mira.retrieve_documents_HYDE(ques.question)
    
    # generate the answer from query
    answer = mira.ask_query(ques.question,docs)
    
    #add_message(answer,"AI",ques.conversation_id)
    return {"success":"true","data": answer}
    # except Exception as e:
    #     return {"success":"false","msg":e}


#endpoint for training new pdfs
@app.post('/api/mira/train')
async def training(file: UploadFile = File(...),key: str = Form(...)):
    # verify the key
    if key != os.getenv('MIRA_KEY'):
        return {"success":"false","msg":"Unauthorized"}
    
    # create the repository if not exists
    if not os.path.exists(os.getenv('UPLOAD_DIRECTORY')):
        os.makedirs(os.getenv('UPLOAD_DIRECTORY'))
    
    file_location = f"{os.getenv('UPLOAD_DIRECTORY')}{file.filename}"
    
    # return if file already exists
    if os.path.exists(file_location):
        return {"success":"false","msg":"File already exists!"}
    
    # save the file
    with open(file_location, "wb") as f:
        f.write(await file.read())
    
    # generate the embeddings and save
    res = train_mira(file_location)
    
    if res:
        return {"success":"true","msg":"training completed!"}
    
    return {"success":"false","msg":"something went wrong!"}


# endpoint to display the webpage to access MIRA
@app.get("/mira", response_class=HTMLResponse)
async def get_webpage():
    return HTMLResponse(content=html_content)

@app.get("/mira-chat", response_class=HTMLResponse)
async def get_webpage2():
    return HTMLResponse(content=html_content_convo)