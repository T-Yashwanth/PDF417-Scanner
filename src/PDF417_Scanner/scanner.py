import cv2
import os
import zxing
from src.PDF417_Scanner.config import field_map  # Import the mapping for driver's license fields
from src.PDF417_Scanner import logger  # Import the logger for logging information and exceptions

class BarcodeScanner:
    """
    This class is responsible for scanning a barcode from an image.
    """
    def __init__(self):
        try:
            # Initialize the barcode reader from the zxing library
            self.reader = zxing.BarCodeReader()
            logger.info("BarcodeScanner initialized successfully.")
        except Exception as e:
            # Log and re-raise the error if initialization fails
            logger.exception("Error initializing BarcodeScanner: %s", e)
            raise e

    def scan(self, image_path):
        """
        Scans the barcode from the specified image path.

        :param image_path: Path to the image file containing the barcode.
        :return: The raw barcode data if found; otherwise, None.
        """
        try:
            # Attempt to decode the barcode from the image file
            barcode = self.reader.decode(image_path)
            if barcode and barcode.parsed:
                # Log successful extraction and parsing of barcode data
                logger.info("Barcode data found and parsed: %s", barcode.parsed)
                return barcode.parsed
            else:
                # Log if no barcode was found in the image
                logger.info("No barcode found in the image: %s", image_path)
                return None
        except Exception as e:
            # Log the exception if an error occurs during the scan
            logger.exception("Error scanning barcode from image %s: %s", image_path, e)
            raise e

class VideoBarcodeScanner:
    """
    This class is responsible for scanning PDF417 barcodes from a video file.
    """
    def __init__(self):
        try:
            # Initialize the ZXing barcode reader
            self.reader = zxing.BarCodeReader()
            # Log successful initialization
            logger.info("VideoBarcodeScanner initialized successfully.")
        except Exception as e:
            logger.exception("Error initializing VideoBarcodeScanner: %s", e)
            raise e

    def scan_video(self, video_path):
        """
        Scans for a PDF417 barcode from the specified video file.

        :param video_path: Path to the video file.
        :return: The parsed barcode data if found; otherwise, None.
        """
        # Open the video file
        cap = cv2.VideoCapture(video_path)
        frame_count = 0
        temp_image_path = "temp_frame.png"  # Temporary image file to save frames

        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    logger.info("No more frames to read from the video.")
                    break

                frame_count += 1
                logger.info("Processing frame %s...", frame_count)

                # Convert the frame to grayscale (optional, but can improve detection)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Save the current frame as a temporary image file
                cv2.imwrite(temp_image_path, gray)

                try:
                    # Attempt to decode the PDF417 barcode from the temporary image
                    barcode = self.reader.decode(
                        temp_image_path,
                        try_harder=True,
                        possible_formats=["PDF_417"]
                    )
                    if barcode and barcode.parsed:
                        logger.info("Decoded barcode data in frame %s: %s", frame_count, barcode.parsed)
                        # Optionally, draw the decoded data on the frame for visual feedback
                        cv2.putText(frame, barcode.parsed, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        return barcode.parsed
                    else:
                        logger.info("No barcode detected in frame %s.", frame_count)
                except Exception as e:
                    logger.exception("Error decoding barcode in frame %s: %s", frame_count, e)
                    raise e

                # Display the current frame in a window
                cv2.imshow("PDF417 Barcode Scanner", frame)
                # Exit the loop if the 'q' key is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    logger.info("Quitting barcode scan due to user request.")
                    break
        finally:
            # Release the video capture and close any OpenCV windows
            cap.release()
            cv2.destroyAllWindows()
            # Clean up the temporary image file if it exists
            if os.path.exists(temp_image_path):
                os.remove(temp_image_path)

        logger.info("Barcode scanning completed without finding a barcode.")
        return None

class DriverLicenseParser:
    """
    This class is responsible for parsing driver's license data from the raw barcode text.
    """
    def __init__(self):
        # Load the preconfigured field map from the configuration
        self.field_map = field_map
        logger.info("DriverLicenseParser initialized successfully.")

    def parse_data(self, data):
        """
        Parses the driver's license data using the preconfigured field map.

        :param data: Raw barcode data as a string.
        :return: A formatted string with extracted driver's license details.
        """
        try:
            # List to hold formatted lines of parsed data
            output_lines = ["Driver's License Data:"]
            # Iterate through each line in the provided data
            for line in data.splitlines():
                # For each line, check against each known field prefix in the map
                for prefix, (label, processor) in self.field_map.items():
                    if line.startswith(prefix):
                        try:
                            # Process the remaining text using the processor function
                            value = processor(line[len(prefix):])
                        except Exception as pe:
                            logger.exception("Error processing line '%s': %s", line, pe)
                            value = line[len(prefix):]
                        output_lines.append(f"{label}: {value}")
                        break  # Exit loop once a matching prefix is found
            result = "\n".join(output_lines)
            logger.info("Driver's license data parsed successfully: %s", result)
            return result
        except Exception as e:
            logger.exception("Error parsing driver's license data: %s", e)
            raise e
