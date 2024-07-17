import os
from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from MIRA_QA import MIRA
from training import train_mira

app = FastAPI()

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
        
    file_location = f"files/{file.filename}"
    
    if os.path.exists(file_location):
        return {"success":"false","msg":"File already exists!"}
    
    with open(file_location, "wb") as f:
        f.write(await file.read())
    
    res = train_mira(file_location)
    
    if res:
        return {"success":"true","msg":"training completed!"}
    
    return {"success":"false","msg":"something went wrong!"}
    