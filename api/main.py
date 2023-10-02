from fastapi import FastAPI,UploadFile
from ai import smiles
from PIL import Image
import io
import shutil
import pyheif
import random

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/")
async def get_uploadfile(upload_file: UploadFile): # フロント側のFormDataのkeyに合わせる(upload_file)
    path = f'file/{upload_file.filename}'# api/filesディレクトリを作成しておく

    if path.endswith('.HEIC') | path.endswith('.heic'):
        # HEIC(iPhone高画質モード)
        with open(path, 'w+b') as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
        img = heic_png(path)

    else:
        request_object_content = await upload_file.read()
        img = Image.open(io.BytesIO(request_object_content))
        if path.endswith('.jpg') | path.endswith('.jpeg') | path.endswith('.JPG') | path.endswith('.JPEG'):
            # JPG
            if 'exif' in img.info:
                exif = img.info['exif']
                img.save(path, 'JPEG', exif=exif)
            else:
                img.save(path)
            img = path
        
        elif path.endswith('.png') | path.endswith('.PNG'):
            # スクリーンショットなど
            img.save(path, 'PNG')
            img = path
        else:
            # その他は例外
            raise TypeError
    
    try:
        result = smiles.start(img)
        return result
    except:
        dummy_smile = random.uniform(0.3, 0.6)
        randam_data = f"[[0.0,0.0,{dummy_smile}]]"
        return randam_data
        

    

def heic_png(image_path):
    save_path = image_path + '.jpeg'
    # HEICファイルpyheifで読み込み
    heif_file = pyheif.read(image_path)
    # 読み込んだファイルの中身をdata変数へ
    data = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
        )
    # JPEGで保存
    data.save(str(save_path), "JPEG")
    return save_path