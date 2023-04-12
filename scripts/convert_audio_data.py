from subprocess import run
from pathlib import Path
from scipy.io.wavfile import read


def main():
    # Create a path object from the audio_files directory
    audio_files = Path('audio_files')
    
    # Get all the .webm files in the directory
    webm_files = audio_files.glob('*.webm')

    # run ffmpeg on each file
    for webm_file in webm_files:
        run(['ffmpeg', '-y', '-i', str(webm_file), '-acodec', 'pcm_s16le', '-ac', '1', '-f', 'wav', str(webm_file).replace('.webm', '.wav')])
    

if __name__ == '__main__':
    main()