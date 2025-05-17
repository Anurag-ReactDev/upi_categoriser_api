from fastapi import FastAPI,UploadFile,File
from pydantic import BaseModel
import shutil
import pandas  as pd

import os

app = FastAPI()

@app.get("/hello")
def say_hello():
    return (
        {"message":"👋Hello from FastAPI"}
        )

#define input schema
class GreetInput(BaseModel):
    name :str

@app.post("/greet")
def greetUser(input:GreetInput):
    # input is now a Python object, not raw JSON
    return {"message":f"Hello {input.name}"}

#upload file end-point

# def upload_file(file:UploadFile = File(...)):
    
#     temp_path = f"temp_{file.filename}"
#     # This creates a temporary filename on your server

#     # For example, if the uploaded file is data.csv,
#     # this makes: temp_data.csv
#     with open(temp_path,"wb") as buffer:
#         # This opens a file on your local machine to write into
#         # "wb" means: write binary mode (important for PDFs, images, etc.)
#         # buffer is a file object you can write data into
#         shutil.copyfileobj(file.file, buffer)
#         # This copies the contents of the uploaded file (file.file)
#         # Into your newly created temp file (buffer)
#         # shutil.copyfileobj is a fast, memory-efficient way to transfer file data
#     return {
#         "filename": file.filename,
#         "message": f"✅ File '{file.filename}' uploaded successfully."
#     }

#upload and parsing

@app.post("/upload-file")
def upload_file(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        df = pd.read_csv(temp_path)
        #read the csv file
        
    except Exception as e:
        #delete file
        os.remove(temp_path)
        return {"error": f"❌ Failed to read CSV: {str(e)}"}

    #delete file after forming DataFrame
    os.remove(temp_path)
    #return summary
    return {
        "rows" : df.shape[0],
        "columns" : df.columns.tolist(),
        "preview" : df.head(5).to_dict(orient="records")
    }