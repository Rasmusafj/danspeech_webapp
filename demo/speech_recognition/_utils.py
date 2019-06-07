import scipy.io.wavfile as wav


def load_audio(path):
    _, sound = wav.read(path)

    if len(sound.shape) > 1:
        if sound.shape[1] == 1:
            sound = sound.squeeze()
        else:
            sound = sound.mean(axis=1)  # multiple channels, average

    return sound.astype(float)
