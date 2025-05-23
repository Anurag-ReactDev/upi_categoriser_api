from fastapi import FastAPI,UploadFile,File
from pydantic import BaseModel
import shutil
import pandas  as pd

import os

app = FastAPI()



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