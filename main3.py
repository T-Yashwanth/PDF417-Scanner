# Filename: main.py
# Required Libraries:
#   pip install fastapi uvicorn python-multipart

from fastapi import FastAPI, File, UploadFile
import uvicorn
import os
from datetime import datetime

app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Create a timestamp string (e.g. "2025-02-02_13-45-30")
    current_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Directory where the uploaded files will be saved
    save_directory = "uploaded_files"
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Construct full file path with date/time prefix
    file_path = os.path.join(save_directory, f"{current_timestamp}_{file.filename}")

    # Read and write file
    with open(file_path, "wb") as f:
        file_content = await file.read()
        f.write(file_content)

    return {
        "filename": file.filename,
        "saved_as": file_path,
        "timestamp": current_timestamp
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)