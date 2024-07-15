from app import app
import uvicorn

@app.get('/')
def home():
    return "hello world!!!"


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True,debug=True)