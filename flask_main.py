from flask import Flask, request, render_template_string, redirect, url_for, jsonify
from datetime import datetime
import os

# Imports from your barcode scanner library
# Adjust as needed based on your actual paths & module names
from src.PDF417_Scanner.scanner import BarcodeScanner, DriverLicenseParser

app = Flask(__name__)

# Minimal inline HTML templates for simplicity
UPLOAD_FORM_TEMPLATE = """
<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Driver's License Barcode Scanner</title>
    </head>
    <body>
        <h1>Upload an Image to Scan</h1>
        <form action="{{ url_for('scan_driver_license') }}" method="post" enctype="multipart/form-data">
            <label>Select an image containing the PDF417 barcode:
                <input type="file" name="file" accept="image/*" required>
            </label>
            <button type="submit">Scan Barcode</button>
        </form>
    </body>
</html>
"""

RESULT_TEMPLATE = """
<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Scan Results</title>
    </head>
    <body>
        <h1>Scan Results</h1>
        {% if error %}
            <p style="color:red;">{{ error }}</p>
        {% else %}
            <p style="color:green;">{{ message }}</p>
            <pre>{{ parsed_data }}</pre>
        {% endif %}
        <a href="{{ url_for('index') }}">Go Back</a>
    </body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    """Render the file upload form."""
    return render_template_string(UPLOAD_FORM_TEMPLATE)

@app.route("/scan-driver-license", methods=["POST"])
def scan_driver_license():
    """Handle the uploaded file, save it, scan the barcode, and parse it."""
    if "file" not in request.files:
        return render_template_string(RESULT_TEMPLATE, error="No file part in request.")

    file = request.files["file"]
    if file.filename == "":
        return render_template_string(RESULT_TEMPLATE, error="No file selected.")

    # Create a date-time string to prepend to the filename
    current_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Directory to store the uploaded files
    save_directory = "uploaded_files"
    os.makedirs(save_directory, exist_ok=True)

    # Construct the full path: e.g., "uploaded_files/2025-02-02_13-45-30_filename.jpg"
    saved_file_path = os.path.join(save_directory, f"{current_timestamp}_{file.filename}")

    try:
        # Save the file permanently
        file.save(saved_file_path)
    except Exception as e:
        return render_template_string(RESULT_TEMPLATE, error=f"File save error: {str(e)}")

    # Scan the barcode
    try:
        barcode_data = BarcodeScanner().scan(saved_file_path)
        if not barcode_data:
            return render_template_string(
                RESULT_TEMPLATE,
                error="No barcode found or barcode could not be parsed."
            )

        # Parse the driver's license data
        parsed_data = DriverLicenseParser().parse_data(barcode_data)

        return render_template_string(
            RESULT_TEMPLATE,
            message="Barcode scanned successfully.",
            parsed_data=parsed_data
        )
    except Exception as e:
        return render_template_string(RESULT_TEMPLATE, error=f"Scan/Parse Error: {str(e)}")
    
@app.route("/scan-driver-license-json", methods=["POST"])
def scan_driver_license_json():
    """Handle the uploaded file and return only JSON output."""
    if "file" not in request.files:
        return jsonify({"error": "No file part in request."}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    current_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    save_directory = "uploaded_files"
    os.makedirs(save_directory, exist_ok=True)
    saved_file_path = os.path.join(save_directory, f"{current_timestamp}_{file.filename}")

    try:
        file.save(saved_file_path)
    except Exception as e:
        return jsonify({"error": f"File save error: {str(e)}"}), 500

    try:
        barcode_data = BarcodeScanner().scan(saved_file_path)
        if not barcode_data:
            return jsonify({"error": "No barcode found or could not be parsed."}), 400

        parsed_data = DriverLicenseParser().parse_data(barcode_data)

        return jsonify({
            "message": "Barcode scanned successfully.",
            "parsed_data": parsed_data
        }), 200
    except Exception as e:
        return jsonify({"error": f"Scan/Parse Error: {str(e)}"}), 500

# Run the Flask server (debug mode for local testing)
if __name__ == "__main__":
    # Replace host/port as needed
    app.run(debug=True, host="127.0.0.1", port=5000)