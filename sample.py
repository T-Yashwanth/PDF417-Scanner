def parse_drivers_license_data(data):
    # Mapping of field prefixes to (Friendly Field Name, Processing Function)
    # The processing function takes the raw string (after the prefix) and returns a formatted version.
    field_map = {
        "DAQ": ("License Number", lambda s: s),
        "DCS": ("Last Name", lambda s: s),
        "DDF": ("First Name", lambda s: s),
        "DBB": ("Date of Birth", lambda s: f"{s[0:2]}/{s[2:4]}/{s[4:]}"),  # Assuming MMDDYYYY without delimiters
        "DAG": ("Street Address", lambda s: s),
        "DAI": ("City", lambda s: s),
        "DAJ": ("State", lambda s: s),
        "DAK": ("Zip", lambda s: s),
        "DBA": ("Expiration Date", lambda s: f"{s[0:2]}/{s[2:4]}/{s[4:]}"),  # Assuming MMDDYYYY
        "DBC": ("Gender", lambda s: s),
        "DAU": ("Height", lambda s: s),
        "DAY": ("Eye Color", lambda s: s),
        "DAW": ("Weight", lambda s: s),
        "DCK": ("Document Description", lambda s: s),
    }

    output_lines = ["Driver's License Data:"]
    # Process each line individually
    for line in data.splitlines():
        # For each known prefix, check if the current line starts with it.
        for prefix, (label, processor) in field_map.items():
            if line.startswith(prefix):
                # Remove the prefix and process the remaining text.
                value = processor(line[len(prefix):])
                output_lines.append(f"{label}: {value}")
                break  # Found a match; move on to the next line.

    return "\n".join(output_lines)


# Example usage:
data = """@ ANSI 636026080102DL00410288ZN03290015DLDAQD12345678
DCSPUBLIC
DDFNJOHN Q
DCSDOE
DAD
DBD01062015
DBB07051980
DBC1
DAYBROWN
DAU180
DAG1234 MAIN ST
DAIANYTOWN
DAJCA
DAK90210"""

print(parse_drivers_license_data(data))