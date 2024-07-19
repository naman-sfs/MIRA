import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from MIRA_QA import MIRA
from training import train_mira
from mira_view import html_content

app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://ec2-3-106-224-103.ap-southeast-2.compute.amazonaws.com:8000"
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
    

@app.post('/api/mira/ask')
async def mira(ques:Question):
    mira = MIRA()
    # try:
    if ques.key != os.getenv('MIRA_KEY'):
        return {"success":"false","msg":"Unauthorized"}
    
    docs = mira.retrieve_documents_HYDE(ques.question)
    
    answer = mira.ask_query(ques.question,docs)
    
    return {"success":"true","data": answer}
    # except Exception as e:
    #     return {"success":"false","msg":e}
    
    
@app.post('/api/mira/train')
async def training(file: UploadFile = File(...),key: str = Form(...)):
    if key != os.getenv('MIRA_KEY'):
        return {"success":"false","msg":"Unauthorized"}
    
    if not os.path.exists(os.getenv('UPLOAD_DIRECTORY')):
        os.makedirs(os.getenv('UPLOAD_DIRECTORY'))
        
    file_location = f"{os.getenv('UPLOAD_DIRECTORY')}{file.filename}"
    
    if os.path.exists(file_location):
        return {"success":"false","msg":"File already exists!"}
    
    with open(file_location, "wb") as f:
        f.write(await file.read())
    
    res = train_mira(file_location)
    
    if res:
        return {"success":"true","msg":"training completed!"}
    
    return {"success":"false","msg":"something went wrong!"}
    
    
@app.get("/mira", response_class=HTMLResponse)
async def get_webpage():
    return HTMLResponse(content=html_content)