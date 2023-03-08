from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import Recording
from django.core.files import File
import settings

import random


def index(request):
    template = loader.get_template('index.html')
    with open(settings.MEDIA_ROOT + "transcriptions.txt", 'r', encoding="utf-8") as f:
        django_file = File(f)
        transcriptions = django_file.readlines()

    transcriptions = [line.rstrip() for line in transcriptions]

    random.shuffle(transcriptions)

    content = {
        "transcriptions": transcriptions[:150],
    }

    return HttpResponse(template.render(content, request))


def requirements(request):
    template = loader.get_template('requirements.html')
    return HttpResponse(template.render({}, request))


def save_audio(request):
    """Save recorded audio blob sent by user."""
    audio_file = request.FILES.get('recorded_audio')
    transcription = request.POST.get("transcription")
    recording = Recording()
    recording.recorded_file = audio_file
    recording.transcription = transcription
    recording.save()

    return JsonResponse({
        'success': True,
    })
