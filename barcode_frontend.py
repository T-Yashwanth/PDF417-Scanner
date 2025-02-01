import streamlit as st
import zxing
import os

def parse_drivers_license_data(data):
    # Example parsing logic for AAMVA format
    # This is a simplified example; actual parsing depends on the specific format
    lines = data.split("\n")
    parsed_output = []
    parsed_output.append("Driver's License Data:\n")
    for line in lines:
        if line.startswith("DAC"):  # Example: First Name
            parsed_output.append(f"First Name: {line[3:]}\n")
        elif line.startswith("DCS"):  # Example: Last Name
            parsed_output.append(f"Last Name: {line[3:]}\n")
        elif line.startswith("DBB"):  # Example: Date of Birth
            parsed_output.append(f"Date of Birth: {line[3:5]}/{line[5:7]}/{line[7:]}\n")
        elif line.startswith("DAG"):  # Example: Street Address
            parsed_output.append(f"Street Address: {line[3:]}\n")
        elif line.startswith("DAQ"):  # Example: License Number
            parsed_output.append(f"License Number: {line[3:]}\n")
        elif line.startswith("DAI"):  # Example: City
            parsed_output.append(f"City: {line[3:]}\n")
        elif line.startswith("DAJ"):  # Example: State
            parsed_output.append(f"State: {line[3:]}\n")
        elif line.startswith("DAK"):  # Example: ZIP
            parsed_output.append(f"Zip: {line[3:]}\n")
        elif line.startswith("DBA"):  # Example: Expiration Date
            parsed_output.append(f"Expiration Date: {line[3:5]}/{line[5:7]}/{line[7:]}\n")
        elif line.startswith("DBc"):  # Example: Gender
            parsed_output.append(f"Gender: {line[3:]}\n")
        elif line.startswith("DAU"):  # Example: Height
            parsed_output.append(f"Height: {line[3:]}\n")
        elif line.startswith("DAY"):  # Example: Eye Color
            parsed_output.append(f"Eye Color: {line[3:]}\n")
        elif line.startswith("DAW"):  # Example: Weight
            parsed_output.append(f"Weight: {line[3:]}\n")
        elif line.startswith("DCK"):  # Example: Document Description
            parsed_output.append(f"Document Description: {line[3:]}\n")
            # Add more fields as needed

    return "\n".join(parsed_output)

def scan_barcode(image_path):
    # Initialize the barcode reader
    reader = zxing.BarCodeReader()

    # Decode the barcode from the image
    barcode = reader.decode(image_path)

    # Check if a barcode was found
    if barcode and barcode.parsed:
        result = [
            #f"**Barcode Type:** {barcode.format}",
            #f"**Barcode Data:** {barcode.parsed}",
            parse_drivers_license_data(barcode.parsed)
        ]
        return "\n".join(result)
    else:
        return "No barcode found in the image."

def main():
    st.title("Driver's License Barcode Scanner")
    st.write("Upload an image containing the Clear barcode, then click 'Scan Barcode'.")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        # Temporarily save the uploaded file
        with open("temp_image.jpg", "wb") as f:
            f.write(uploaded_file.read())

        if st.button("Scan Barcode"):
            results = scan_barcode("temp_image.jpg")
            st.markdown(results)

        # Clean up the file after usage
        if os.path.exists("temp_image.jpg"):
            os.remove("temp_image.jpg")

if __name__ == "__main__":
    main()

# Created/Modified files during execution:
# 1. temp_image.jpg (temporary file to store user-uploaded image)