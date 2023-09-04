from fastapi import FastAPI,UploadFile
from ai import smiles
import shutil

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/")
def get_uploadfile(upload_file: UploadFile): # フロント側のFormDataのkeyに合わせる(upload_file)
    path = f'file/{upload_file.filename}'# api/filesディレクトリを作成しておく
    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    result = smiles.start(path)
    return result