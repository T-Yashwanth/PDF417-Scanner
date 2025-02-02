
Install java in your system

Deactivate base version if you have one
```bash
conda deactivate
```

Create Virtual Environment
```bash
python -m venv PDF415_scanner
```

Activate Virtual Environment
```bash
.\PDF415_scanner\Scripts\activate
```
for git bash
```bash
source PDF415_scanner/Scripts/activate
```

Install requirements
```bash
pip install -r requirements.txt
```

```bash
streamlit run main.py
```

Flask front end and curl
```bash
python flask_main.py
```
```bash
curl -X POST \
     -F "file=@C:/Users/yash/Downloads/Projects/ID project/test2.jpg" \
     http://127.0.0.1:5000/scan-driver-license
```
```bash
curl -X POST \
     -F "file=@C:/Users/yash/Downloads/Projects/ID project/test2.jpg" \
     http://127.0.0.1:5000/scan-driver-license-json
```