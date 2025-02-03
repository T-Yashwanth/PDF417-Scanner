from flask import Flask, request, render_template, redirect, url_for, jsonify
from datetime import datetime
import os
from src.PDF417_Scanner.scanner import BarcodeScanner, VideoBarcodeScanner, DriverLicenseParser

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    """Render the image file upload form."""
    return render_template("templates.html", template="upload_form")

@app.route("/upload-video", methods=["GET"])
def upload_video():
    """Render the video file upload form."""
    return render_template("templates.html", template="video_upload_form")

@app.route("/scan-driver-license", methods=["POST"])
def scan_driver_license():
    """Handle the uploaded image file, scan the barcode, and parse it."""
    if "file" not in request.files:
        return render_template("templates.html", template="result", error="No file part in request.")

    file = request.files["file"]
    if file.filename == "":
        return render_template("templates.html", template="result", error="No file selected.")

    current_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    save_directory = "uploaded_files"
    os.makedirs(save_directory, exist_ok=True)
    saved_file_path = os.path.join(save_directory, f"{current_timestamp}_{file.filename}")

    try:
        file.save(saved_file_path)
    except Exception as e:
        return render_template("templates.html", template="result", error=f"File save error: {str(e)}")

    try:
        barcode_data = BarcodeScanner().scan(saved_file_path)
        if not barcode_data:
            return render_template("templates.html", template="result", error="No barcode found or barcode could not be parsed.")

        parsed_data = DriverLicenseParser().parse_data(barcode_data)
        return render_template("templates.html", template="result", message="Barcode scanned successfully.", parsed_data=parsed_data)
    except Exception as e:
        return render_template("templates.html", template="result", error=f"Scan/Parse Error: {str(e)}")

@app.route("/scan-driver-license-json", methods=["POST"])
def scan_driver_license_json():
    """Handle the uploaded image file and return only JSON output."""
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
        return jsonify({"message": "Barcode scanned successfully.", "parsed_data": parsed_data}), 200
    except Exception as e:
        return jsonify({"error": f"Scan/Parse Error: {str(e)}"}), 500

@app.route("/scan-driver-license-video", methods=["POST"])
def scan_driver_license_video():
    """Handle the uploaded video file, scan the barcode, and parse it."""
    if "file" not in request.files:
        return render_template("templates.html", template="result", error="No file part in request.")

    file = request.files["file"]
    if file.filename == "":
        return render_template("templates.html", template="result", error="No file selected.")

    current_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    save_directory = "uploaded_files"
    os.makedirs(save_directory, exist_ok=True)
    saved_file_path = os.path.join(save_directory, f"{current_timestamp}_{file.filename}")

    try:
        file.save(saved_file_path)
    except Exception as e:
        return render_template("templates.html", template="result", error=f"File save error: {str(e)}")

    try:
        barcode_data = VideoBarcodeScanner().scan_video(saved_file_path)
        if not barcode_data:
            return render_template("templates.html", template="result", error="No barcode found in video or barcode could not be parsed.")

        parsed_data = DriverLicenseParser().parse_data(barcode_data)
        return render_template("templates.html", template="result", message="Barcode scanned successfully from video.", parsed_data=parsed_data)
    except Exception as e:
        return render_template("templates.html", template="result", error=f"Scan/Parse Error: {str(e)}")

@app.route("/scan-driver-license-video-json", methods=["POST"])
def scan_driver_license_video_json():
    """Handle the uploaded video file and return JSON output."""
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
        barcode_data = VideoBarcodeScanner().scan_video(saved_file_path)
        if not barcode_data:
            return jsonify({"error": "No barcode found in video or could not be parsed."}), 400

        parsed_data = DriverLicenseParser().parse_data(barcode_data)
        return jsonify({"message": "Barcode scanned successfully from video.", "parsed_data": parsed_data}), 200
    except Exception as e:
        return jsonify({"error": f"Scan/Parse Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)