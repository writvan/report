from django.db import models
from django.contrib.auth.models import User

class UserFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='user_files/')

