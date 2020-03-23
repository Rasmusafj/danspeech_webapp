# Danspeech
Webapp for data collection

## Guide 
Note that this is a quick guide to get you started and there might be a few errors. In that case or if any generel questions, feel free to create issues on this github repo and I will try to fix / help you. 

Note, you should definetly use chrome or firefox!

### Requirements
* django which can be installed through pip or conda

### Getting started
* Run python manage.py migrate (this will create the db)
* (optional) Run python manage.py createsuperuser (super user if you want to access the admin side / monitoring)
* Run python manage.py runserver (this will launch the wepapp on port http://127.0.0.1:8000/

### Audio files
The audio files are saved in .webm format. If i remember correctly, then they are saved as mono files with 44100kHz. So you may use e.g. ffmpeg to convert them to .wav files afterwards.

### Modifying presented text in the webapp
To modify the presented text, edit the `danspeech_webapp/audio_files/transcriptions.txt` file. The text presented in the webapp is randomly sampled from that file.
