from django.db import models

class VideoUpload(models.Model):
    original = models.FileField(upload_to='uploads/')
    transcoded = models.FileField(upload_to='transcoded/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)