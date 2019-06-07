from django.http import HttpResponse, JsonResponse
from django.template import loader
import subprocess
import settings
import os

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

# Create your views here.
def index(request):
    template = loader.get_template('demo_index.html')
    return HttpResponse(template.render({}, request))


def preprocess_webm(request):
    old_file = os.path.join(settings.MEDIA_ROOT, "tmp.webm")
    if os.path.isfile(old_file):
        os.remove(os.path.join(settings.MEDIA_ROOT, "tmp.webm"))

    audio_file = request.FILES.get('recorded_audio')
    path = default_storage.save('tmp.webm', ContentFile(audio_file.read()))
    tmp_file = os.path.join(settings.MEDIA_ROOT, path)
    dest = os.path.join(settings.MEDIA_ROOT, "temp.wav")
    command = "ffmpeg -y -i {0} -acodec pcm_s16le -ac 1 -ar 16000 -f wav {1}".format(tmp_file, dest)
    subprocess.call(command, shell=True)

    return JsonResponse({
        'success': True,
    })


def transcribe(request):
    return JsonResponse({
        'success': True,
    })