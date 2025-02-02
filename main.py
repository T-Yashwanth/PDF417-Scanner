from src.PDF417_Scanner.config import image_path
from src.PDF417_Scanner.scanner import BarcodeScanner, DriverLicenseParser
from src.PDF417_Scanner import logger
import streamlit as st
import os


# Use this if you want to test with image path and in cmd output with any frontend
#a = BarcodeScanner().scan(image_path)
#print(DriverLicenseParser().parse_data(a))

def main():
    try:
        # Set the title and instructions for the app
        st.title("Driver's License Barcode Scanner")
        st.write("Upload an image containing the Clear barcode, then click 'Scan Barcode'.")

        # Allow user to upload an image file
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

        # Proceed only if a file was uploaded
        if uploaded_file:
            try:
                # Temporarily save the uploaded image to disk
                with open("temp_image.jpg", "wb") as f:
                    f.write(uploaded_file.read())
                logger.info("Uploaded file saved successfully as temp_image.jpg.")
            except Exception as e:
                # Log exception and display error message to the user
                logger.exception("Error saving uploaded file: %s", e)
                st.error("Error processing file. Please try again.")
                return

            # When the user clicks the button to scan the uploaded barcode
            if st.button("Scan Barcode"):
                try:
                    # Scan the barcode from the temporarily saved image
                    barcode_data = BarcodeScanner().scan("temp_image.jpg")
                    if barcode_data:
                        # Parse the driver's license data if barcode scanning was successful
                        parsed_result = DriverLicenseParser().parse_data(barcode_data)
                        st.markdown(parsed_result)
                    else:
                        st.error("No barcode found or barcode could not be parsed.")
                except Exception as e:
                    # Log any error during barcode scanning and parsing, and show an error message
                    logger.exception("Error scanning and parsing the barcode: %s", e)
                    st.error("An error occurred while scanning the barcode. Please try again.")

            # Attempt to remove the temporary file after processing
            try:
                if os.path.exists("temp_image.jpg"):
                    os.remove("temp_image.jpg")
                    logger.info("Temporary file temp_image.jpg removed successfully.")
            except Exception as e:
                logger.exception("Error removing temporary file: %s", e)
                st.warning("Temporary file could not be removed. Please check file permissions.")

    except Exception as e:
        # Catch any unexpected exceptions in the main function
        logger.exception("Unhandled exception in main: %s", e)
        st.error("An unexpected error occurred. Please try again later.")

if __name__ == "__main__":
    main()
