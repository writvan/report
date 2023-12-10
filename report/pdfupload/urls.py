# pdfupload/urls.py
from django.urls import path
from .views import upload_file

app_name = 'pdfupload'  # Add this line if it's not present

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),  # Ensure a name is assigned
    # Add other URL patterns as needed
]
