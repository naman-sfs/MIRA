from app import app
import uvicorn
import os

@app.get('/')
def home():
    return "hello world!!!"


if __name__ == "__main__":
    uvicorn.run("main:app", host=os.getenv('HOST_IP'), port=8080, reload=True)