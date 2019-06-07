from django.http import HttpResponse, JsonResponse
from django.template import loader
import subprocess
import settings
import os

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from .speech_recognition.danspeech_demo import DanSpeechDemo

danspeech_model = DanSpeechDemo()

def index(request):
    template = loader.get_template('demo_index.html')
    return HttpResponse(template.render({}, request))


def preprocess_webm(request):
    old_file = os.path.join(settings.MEDIA_ROOT, "tmp.webm")
    if os.path.isfile(old_file):
        os.remove(old_file)

    audio_file = request.FILES.get('recorded_audio')
    path = default_storage.save('tmp.webm', ContentFile(audio_file.read()))
    tmp_file = os.path.join(settings.MEDIA_ROOT, path)
    dest = os.path.join(settings.MEDIA_ROOT, "temp.wav")
    command = "ffmpeg -y -i {0} -acodec pcm_s16le -ac 1 -ar 16000 -f wav {1}".format(tmp_file, dest)
    subprocess.call(command, shell=True)

    return JsonResponse({
        'success': True,
    })


def update_config(request):
    model = request.POST["model_choice"]
    lm = request.POST["language_model"]
    alpha = request.POST["alpha"]
    beta = request.POST["beta"]

    return HttpResponse(status=204)


def transcribe(request):
    #print("WHY???")
    #danspeech_model = DanSpeechDemo()
    transcription = danspeech_model.transcribe()

    return JsonResponse({
        'success': True,
        'trans': transcription
    })