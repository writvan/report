# pdfupload/views.py

from django.shortcuts import render, redirect
from .forms import UploadFileForm
from pdfminer.high_level import extract_text
from pdfminer.pdfdocument import PDFPasswordIncorrect
import enchant
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
# pdfupload/views.py
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from pdfminer.high_level import extract_text
from pdfminer.pdfdocument import PDFPasswordIncorrect
from spellchecker import SpellChecker 
from .models import DocumentDetails, DocumentCorrections

@login_required(login_url='login')
def upload_file(request):
    errors = []
    num_words = 0
    spelling_errors = []
    corrected_spelling_errors = {}  # Initialize corrected_spelling_errors

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()

            # Perform PDF content checks
            pdf_path = uploaded_file.pdf_file.path
            errors, num_words, spelling_errors = check_pdf_content(pdf_path)

            # Correct spelling errors using SpellChecker
            corrected_spelling_errors = correct_spelling_errors(spelling_errors)

             # Save document details
            doc_details = DocumentDetails.objects.create(
                doc_name=uploaded_file.pdf_file.name,
                num_words=num_words
            )

            # Save document corrections
            DocumentCorrections.objects.create(
                doc_details=doc_details,
                spell_errors=spelling_errors,
                corrections=corrected_spelling_errors
            )


    else:
        form = UploadFileForm()

    return render(request, 'pdfupload/upload.html', {
        'form': form,
        'errors': errors,
        'num_words': num_words,
        'spelling_errors': spelling_errors,
        'corrected_spelling_errors': corrected_spelling_errors.items(),  # Convert to key-value pairs
    })

def correct_spelling_errors(spelling_errors):
    spell = SpellChecker()
    corrected_spelling_errors = {}
    
    for error in spelling_errors:
        corrected_word = spell.correction(error)
        corrected_spelling_errors[error] = corrected_word

    return corrected_spelling_errors
def check_pdf_content(pdf_path):
    errors = []
    num_words = 0
    spelling_errors = []
    try:
        with open(pdf_path, 'rb') as file:
            text = extract_text(file)

            # Count the number of words
            num_words = count_words(text)

            # Check font family
            font_family_errors = check_font_family(text)
            errors.extend(font_family_errors)

            # Check font size and justification for regular text and headings
            text_errors = check_text_format(text)
            errors.extend(text_errors)

            # Check spelling errors using multiple dictionaries
            spelling_errors = check_spelling_errors(text, ['en_US', 'en_GB'])
            if spelling_errors:
                errors.append('There are spelling errors ')

    except PDFPasswordIncorrect:
        errors.append('The PDF is password-protected. Please provide the password.')

    return errors, num_words, spelling_errors

    
def count_words(text):
    # Simple word count, you might want to enhance this based on your requirements
    words = [word.strip('.,?!()[]{}') for word in text.split() if word.strip('.,?!()[]{}')]
    return len(words)

def check_font_family(text):
    errors = []
    expected_font_family = 'Arial'

    font_family_lines = [line.strip() for line in text.split('\n') if line.strip() and line.strip().endswith('Tf')]
    for font_family_line in font_family_lines:
        font_family = font_family_line.split(' ')[-2]
        if font_family.lower() != expected_font_family.lower():
            errors.append('Text font should be Arial.')

    return errors


def check_text_format(text):
    errors = []
    expected_text_font_size = 14
    expected_text_justification = 'Justified'
    expected_heading_font_size = 20
    expected_heading_boldness = True  # Assuming True for bold, adjust as needed
    expected_heading_alignment = 'Center'

    text_lines = [line.strip() for line in text.split('\n') if line.strip()]
    for text_line in text_lines:
        try:
            font_size = int(text_line.split(' ')[-1])
        except ValueError:
            # Skip lines where the font size cannot be converted to an integer
            continue

        if font_size == expected_text_font_size:
            justification = ' '.join(text_line.split(' ')[-3:-1])
            if justification != expected_text_justification:
                errors.append('Text is not proper: Font size should be 14 and justified.')
        elif font_size == expected_heading_font_size:
            boldness = 'BT' in text_line  # Assuming 'BT' indicates bold, adjust as needed
            alignment = text_line.split(' ')[-4]
            if boldness != expected_heading_boldness or alignment != expected_heading_alignment:
                errors.append('Heading is not proper: Font size should be 20, bold, and aligned in the center.')

    return errors

import string
# pdfupload/views.py

def check_spelling_errors(text, dictionary_langs):
    errors = []
    # Initialize spellcheckers for each specified dictionary
    spell_checkers = [enchant.Dict(lang) for lang in dictionary_langs]

    # Extract words from the text and check for spelling errors
    words = [word.strip(string.punctuation) for word in text.split() if word.strip(string.punctuation)]

    if not words:
        return errors  # No need to check spelling for an empty list of words

    # Collect misspelled words for each dictionary
    misspelled_words_by_dictionary = {lang: set() for lang in dictionary_langs}
    
    for word in words:
        for i, spell_checker in enumerate(spell_checkers):
            if not spell_checker.check(word):
                misspelled_words_by_dictionary[dictionary_langs[i]].add(word)

    # Find words that are not present in both dictionaries
    common_misspellings = set.intersection(*misspelled_words_by_dictionary.values())
    
    if common_misspellings:
        errors.extend(common_misspellings)

    return errors

