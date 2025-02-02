
# Example usage
image_path = "Drivers Licence Back.jpg"  # Replace with the path to your image

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