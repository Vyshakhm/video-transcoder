# video_app/views.py

import os
import subprocess
from django.shortcuts import render
from django.conf import settings
from .forms import VideoUploadForm

def transcode_video(input_path, output_path, output_format):
    format = output_format.lower()

    if format == 'avi':
        codec_args = ['-c:v', 'mpeg4', '-qscale:v', '5', '-c:a', 'mp3']
    elif format == 'webm':
        # Strict browser-compatible webm
        codec_args = [
            '-c:v', 'libvpx',        # Use VP8 for broader support
            '-b:v', '1M',
            '-c:a', 'libvorbis'      # Audio must be Vorbis for VP8
        ]
    elif format == 'mp4':
        codec_args = ['-c:v', 'libx264', '-crf', '23', '-preset', 'medium', '-c:a', 'aac']
    elif format == 'mov':
        codec_args = ['-c:v', 'libx264', '-c:a', 'aac']
    else:
        raise ValueError(f"Unsupported format: {format}")

    command = ['ffmpeg', '-y', '-i', input_path] + codec_args + [output_path]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        print("FFmpeg error:", result.stderr.decode())
        raise Exception("FFmpeg failed:\n" + result.stderr.decode())



def upload_video(request):
    context = {}
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['video']
            output_format = form.cleaned_data['format'].lower().strip('.')
            input_path = os.path.join(settings.MEDIA_ROOT, 'uploads', uploaded_file.name)
            os.makedirs(os.path.dirname(input_path), exist_ok=True)

            # Save uploaded video
            with open(input_path, 'wb+') as dest:
                for chunk in uploaded_file.chunks():
                    dest.write(chunk)

            # Set output path
            base_name = os.path.splitext(uploaded_file.name)[0]
            output_filename = f"{base_name}_converted.{output_format}"
            output_path = os.path.join(settings.MEDIA_ROOT, 'transcoded', output_filename)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            try:
                transcode_video(input_path, output_path, output_format)
                context['output_video'] = os.path.join(settings.MEDIA_URL, 'transcoded', output_filename)

                if output_format == 'avi':
                    context['note'] = "AVI format is not supported in browsers. Please download and play it locally."

            except Exception as e:
                context['error'] = str(e)
    else:
        form = VideoUploadForm()

    context['form'] = form
    return render(request, 'video_app/upload.html', context)
