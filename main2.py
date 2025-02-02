# Filename: main.py
# Run with: uvicorn main:app --reload

import os
import uvicorn
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, HTTPException
from src.PDF417_Scanner.scanner import BarcodeScanner, DriverLicenseParser
from src.PDF417_Scanner import logger

app = FastAPI()

@app.post("/scan-driver-license/")
async def scan_driver_license(file: UploadFile = File(...)):
    """
    Upload an image containing the PDF417 barcode from a driver's license,
    parse it, and return the extracted data. The uploaded file is stored
    permanently on the server (not deleted).
    """
    # Create a date-time string to prepend to the filename
    current_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Directory to store the uploaded files
    save_directory = "uploaded_files"
    os.makedirs(save_directory, exist_ok=True)

    # Construct the full path: e.g. "uploaded_files/2025-02-02_13-45-30_filename.jpg"
    saved_file_path = os.path.join(save_directory, f"{current_timestamp}_{file.filename}")

    try:
        # Read the uploaded file and save it permanently
        with open(saved_file_path, "wb") as f:
            f.write(await file.read())
        logger.info("Uploaded file saved: %s", saved_file_path)

    except Exception as save_err:
        logger.exception("Error saving uploaded file: %s", save_err)
        raise HTTPException(
            status_code=500,
            detail="An error occurred while saving the uploaded file."
        )

    try:
        # Scan the barcode from the saved image
        barcode_data = BarcodeScanner().scan(saved_file_path)
        if not barcode_data:
            # If we can't scan or find any barcode data, return 400
            raise HTTPException(
                status_code=400,
                detail="No barcode found or barcode could not be parsed."
            )

        # Parse the driver's license data
        parsed_data = DriverLicenseParser().parse_data(barcode_data)

        return {
            "message": "Barcode scanned successfully.",
            "parsed_data": parsed_data
        }

    except Exception as scan_err:
        logger.exception("Error scanning/parsing the barcode: %s", scan_err)
        raise HTTPException(
            status_code=500,
            detail="An error occurred while scanning the barcode."
        )
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)