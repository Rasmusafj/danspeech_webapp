import librosa
import scipy
import torch
import os
import numpy as np
from ._utils import load_audio
from .decoder import GreedyDecoder, BeamCTCDecoder
from .torch_model import DanSpeech
import settings
import speech_recognition as sr
import sys

models_dict = {
            "0": "DanSpeech.pth",
            "1": "baseline.pth",
            "2": "augmented_baseline.pth",
            "3": "1conv.pth",
            "4": "3conv32feat.pth",
            "5": "3convs96feat.pth",
            "6": "3RNN.pth",
            "7": "7RNN.pth",
            "8": "9RNN.pth",
            "9": "400units.pth",
            "10": "1200units.pth",
            "11": "1600units.pth",
            "12": "transfer_learning_0.pth",
            "13": "transfer_learning_3.pth",
            "14": "combined_data.pth",
            "15": "librispeech_batch24_continue.pth",
        }

lm_dict = {
            "0": "dsl-3gram.klm",
            "1": "dsl-5gram.klm",
            "16": "greedy",
            "2": "wiki-3gram.klm",
            "3": "wiki-5gram.klm",
            "4": "leipzig-3gram.klm",
            "5": "leipzig-5gram.klm",
            "6": "wiki_dsl-3gram.klm",
            "7": "wiki_dsl-5gram.klm",
            "8": "dsl_leipzig-3gram.klm",
            "9": "dsl_leipzig-5gram.klm",
            "10": "wiki_leipzig-3gram.klm",
            "11": "wiki_leipzig-5gram.klm",
            "12": "combined-3gram.klm",
            "13": "combined-5gram.klm",
            "14": "3-gram_en.klm",
            "15": "4-gram_en.klm",
        }


class DanSpeechDemo(object):

    def __init__(self):
        self.model_path = "9RNN.pth"
        self.lm = "dsl-5gram.klm"
        self.alpha = 1.3
        self.beta = 0.2

        torch.set_grad_enabled(False)
        self.device = torch.device("cpu")
        self.update_model()

        self.normalize = True
        self.sample_rate = 16000
        self.window = scipy.signal.hamming
        self.window_stride = 0.01
        self.window_size = 0.02
        self.n_fft = int(self.sample_rate*self.window_size)
        self.hop_length = int(self.sample_rate*self.window_stride)
        self.update_decoder()

    def update_decoder(self):
        if self.lm != "greedy":
            self.decoder = BeamCTCDecoder(labels=self.labels, lm_path=os.path.join(settings.LMS_DIR, self.lm),
                                          alpha=self.alpha, beta=self.beta,
                                          beam_width=64, num_processes=6, cutoff_prob=1.0, cutoff_top_n=40)
        else:
            self.decoder = GreedyDecoder(labels=self.labels, blank_index=self.labels.index('_'))

    def update_model(self):
        model = DanSpeech.load_model(os.path.join(settings.MODELS_DIR, self.model_path))
        self.model = model.to(self.device)
        self.model.eval()
        self.labels = self.model.labels


    def update_config(self, lm, model, alpha, beta):
        self.model_path = models_dict[model]
        self.lm = lm_dict[lm]
        self.alpha = float(alpha)
        self.beta = float(beta)

        self.update_model()
        self.update_decoder()


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
        recording = self.parse_audio(recording).contiguous()
        recording = recording.view(1, 1, recording.size(0), recording.size(1))
        recording.to(self.device)
        input_sizes = torch.IntTensor([recording.size(3)]).int()
        out, output_sizes = self.model(recording, input_sizes)
        decoded_output, _ = self.decoder.decode(out, output_sizes)
        return decoded_output[0][0]


class GoogleSpeech():

    def __init__(self):
        google_path = os.path.join(settings.MEDIA_ROOT, "google_key/danspeech_googlekey.json")
        if os.path.isfile(google_path):

            with open(google_path) as f:
                self.gc_credentials = f.read()
        else:
            self.gc_credentials = None

        self.r = sr.Recognizer()

    def transcribe(self):

        if not self.gc_credentials:
            return "Google not available"

        example = sr.AudioFile(os.path.join(settings.MEDIA_ROOT, "temp.wav"))
        with example as source:
            audio = self.r.record(source)

        transcription = self.r.recognize_google_cloud(audio, language="da-DK",
                                                      credentials_json=self.gc_credentials)

        return transcription