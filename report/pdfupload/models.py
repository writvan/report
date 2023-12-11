# pdfupload/models.py

from django.db import models

class UploadedFile(models.Model):
    pdf_file = models.FileField(upload_to='uploads/')
    
class DocumentDetails(models.Model):
    doc_name = models.CharField(max_length=255)
    num_words = models.IntegerField()

class DocumentCorrections(models.Model):
    doc_details = models.ForeignKey(DocumentDetails, on_delete=models.CASCADE)
    spell_errors = models.JSONField()
    corrections = models.JSONField()