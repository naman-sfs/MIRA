import os
from fastapi import FastAPI
from pydantic import BaseModel
from MIRA_QA import MIRA

app = FastAPI()


class Question(BaseModel):
    question: str
    key:str
    

@app.post('/api/mira/ask')
def mira(ques:Question):
    mira = MIRA()

    if ques.key != os.getenv('MIRA_KEY'):
        return {"success":"false","msg":"Unauthorized"}
    
    docs = mira.retrieve_documents_HYDE(ques.question)
    
    answer = mira.ask_query(ques.question,docs)
    
    return {"success":"true","data": answer}

    