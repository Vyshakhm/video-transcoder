# video_app/forms.py

from django import forms

class VideoUploadForm(forms.Form):
    VIDEO_FORMAT_CHOICES = [
        ('mp4', 'MP4'),
        ('avi', 'AVI'),
        ('mov', 'MOV'),
        ('webm', 'WEBM'),
    ]

    video = forms.FileField(label="Select Video File")
    format = forms.ChoiceField(choices=VIDEO_FORMAT_CHOICES, label="Convert to Format")
