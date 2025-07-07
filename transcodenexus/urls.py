# project/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from video_app.views import upload_video

urlpatterns = [
    path('', upload_video, name='upload_video'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
