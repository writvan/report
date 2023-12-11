# PDF Checker Web App

## Overview

The PDF Checker Web App is a Django-based web application that allows users to upload PDF files for analysis. The application performs various checks on the PDF content, including counting words, identifying spelling errors, and providing corrections.

## Features

- **PDF Upload**: Users can upload PDF files through the web interface.
- **Content Analysis**: The application analyzes the content of the uploaded PDF files.
- **Spelling Error Detection**: Spelling errors in the PDF content are identified.
- **Correction Suggestions**: The application suggests corrections for spelling errors.

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/writvan/report.git
   cd report
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply migrations,Run the development server :
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```
The application will be accessible at http://localhost:8000.

Usage
Access the web application in your browser.

Click on the "Get Started" button to navigate to the PDF upload page.

Upload a PDF file and click the "Upload" button.

View the analysis results, including word count, spelling errors, and corrections.

Dependencies
- Django: https://www.djangoproject.com/
- PyMuPDF: https://pymupdf.readthedocs.io/
- PySpellChecker: https://pyspellchecker.readthedocs.io/
- NLTK: https://www.nltk.org/
- License
- This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
Special thanks to OpenAI for providing the language model used in this project.


Feel free to customize this template based on the specific details of your project. Add sections, details, or badges as needed.


## Authors

- [Writvan Ghosh](https://github.com/writvan) - Lead Developer
- [Winston Pais](https://github.com/WPais212) - Full Stack Web Developer
