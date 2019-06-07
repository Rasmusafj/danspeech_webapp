import librosa
import scipy
import torch
import os
import settings
import numpy as np
from ._utils import load_audio
from .decoder import GreedyDecoder, BeamCTCDecoder
from .model import DanSpeech


class DanSpeechDemo(object):
    def __init__(self, transcribe_config=None):
        self.normalize = True
        self.sample_rate = 16000
        self.window = scipy.signal.hamming
        self.window_stride = 0.01
        self.window_size = 0.02
        self.n_fft = int(self.sample_rate*self.window_size)
        self.hop_length = int(self.sample_rate*self.window_stride)

        torch.set_grad_enabled(False)
        self.model = DanSpeech.load_model(transcribe_config.get("model"))
        self.device = torch.device("cpu")
        self.model = self.model.to(self.device)
        self.model.eval()
        self.labels = self.model.labels

        if not transcribe_config:
            transcribe_config = {"lm": "Greedy", "alpha": 1.44, "beta": 0.14, "lm_path": "demo/lms/dsl_3gram.klm"}

        if transcribe_config.get("lm") == "beam":
            self.decoder = BeamCTCDecoder(labels=self.labels, lm_path=transcribe_config.get("lm_path"),
                                          alpha=transcribe_config.get("alpha"), beta=transcribe_config.get("beta"),
                                          beam_width=64, num_processes=6)
        else:
            self.decoder = GreedyDecoder(labels=self.labels, blank_index=self.labels.index('_'))

    def parse_audio(self, recording):
        D = librosa.stft(recording, n_fft=self.n_fft, hop_length=self.hop_length,
                         win_length=self.n_fft, window=self.window)

        spect, phase = librosa.magphase(D)
        spect = np.log1p(spect)
        spect = torch.FloatTensor(spect)
        if self.normalize:
            mean = spect.mean()
            std = spect.std()
            spect.add_(-mean)
            spect.div_(std)

        return spect

    def transcribe(self):
        recording = load_audio(os.path.join(settings.MEDIA_ROOT, "temp.wav"))
        recording = self.parse_audio(recording)
        recording.to(self.device)
        transcription = self.model(recording)

        return self.decoder.decode(transcription.data)
