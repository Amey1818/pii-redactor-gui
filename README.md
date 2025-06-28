# 🕵️ Sensitive Document Auto-Sanitizer (PII Redactor)

A Python-based desktop application that detects and redacts sensitive personal information (PII) from PDF documents using Natural Language Processing (spaCy) and regular expressions. The tool features a user-friendly GUI built with Tkinter and generates a redacted version of the document for safe sharing or storage.

## 📌 Features

- 🔍 Detects PII like:
  - Person names
  - Locations (cities, states)
  - Organizations
  - Email addresses
  - Phone numbers
  - Aadhaar / PAN (via regex)
  
- 🧠 NLP-powered detection using `spaCy`
- 📄 PDF text extraction and redaction using `PyMuPDF`
- 🖥️ GUI dashboard built with `Tkinter` to upload files and preview PII
- 📂 Saves a clean redacted version of the document
- 🔐 Ideal for data privacy, HR, legal, or compliance workflow


## 🚀 How It Works

1. Launch the app by running `gui.py`
2. Upload a PDF document (e.g., a resume or HR file)
3. The tool scans the document and displays detected PII in a table
4. It then creates a redacted PDF in the `docs/` folder with sensitive info hidden



## 🔧 Technologies Used

| Tool        | Purpose                               |
|-------------|----------------------------------------|
| Python      | Main programming language              |
| spaCy       | Named Entity Recognition (NER)         |
| regex       | Custom detection (emails, Aadhaar, PAN)|
| PyMuPDF     | PDF reading and redaction              |
| Tkinter     | GUI development                        |



## 🧠 Why This Project?

In a world driven by data, protecting personal information is critical. This tool automates the process of finding and removing sensitive data from documents, making it useful for:
- HR teams reviewing resumes
- Legal teams handling case files
- Data science workflows needing anonymized data
- GDPR/DPDP compliance workflows


🛠 Installation & Setup
1. Clone the Repository
Open your terminal or command prompt and run:
git clone https://github.com/Amey1818/pii-redactor-gui.git
cd pii-redactor-gui

2. Install Required Python Packages
Make sure you have Python 3.9 or later installed. Then install the necessary libraries:

nginx
Copy
Edit
pip install spacy PyMuPDF fpdf
python -m spacy download en_core_web_sm

Run the Application
To launch the GUI:

nginx
Copy
Edit
python gui.py
This will open a Tkinter-based desktop interface. You can upload a PDF file, view detected PII (like names, emails, phone numbers, etc.), and generate a redacted PDF saved to the docs/ folder.

Notes
Input and output PDF files are handled inside the docs/ folder.
If PII detection is too broad or too strict, you can fine-tune logic inside src/detect_pii.py.
The tool works entirely offline — no data leaves your machine.
