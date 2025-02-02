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
                logger.info("Barcode data found and parsed.%s", barcode.parsed)
                return barcode.parsed
            else:
                # Log if no barcode was found in the image
                logger.info("No barcode found in the image: %s", image_path)
                return None
        except Exception as e:
            # Log the exception if an error occurs during the scan
            logger.exception("Error scanning barcode from image %s: %s", image_path, e)
            raise e

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
                            # Remove the prefix and process the remaining text using the processor function
                            value = processor(line[len(prefix):])
                        except Exception as pe:
                            # Log any exception during processing and default to using the raw substring
                            logger.exception("Error processing line '%s': %s", line, pe)
                            value = line[len(prefix):]
                        # Append the processed information in label: value format to the output list
                        output_lines.append(f"{label}: {value}")
                        break  # Exit loop once a matching prefix is found, and move to the next line

            # Join the processed lines into a single string with newline separators
            result = "\n".join(output_lines)
            logger.info("Driver's license data parsed successfully. %s", result)
            return result

        except Exception as e:
            # Log the exception if an error occurs during parsing
            logger.exception("Error parsing driver's license data: %s", e)
            raise e
