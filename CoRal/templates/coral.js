
transcriptions = [];
{% for transcription in transcriptions %}
transcriptions.push("{{ transcription }}");
{% endfor %}

var current_trans = transcriptions.pop();
$('#transcription').text(current_trans);

var player;
var recorder;
var microphone;
var blob;
var audio = document.getElementById('safariAudio');
var form = document.getElementById('metadata_form');
var oldRecording = false;

function captureMicrophone(callback) {
    if (microphone) {
        callback(microphone);
        return;
    }
    if (typeof navigator.mediaDevices === 'undefined' || !navigator.mediaDevices.getUserMedia) {
        alert('This browser does not supports WebRTC getUserMedia API.');
        if (!!navigator.getUserMedia) {
            alert('This browser seems supporting deprecated getUserMedia API.');
        }
    }
    navigator.mediaDevices.getUserMedia({
        audio: isEdge ? true : {
            echoCancellation: false
        }
    }).then(function (mic) {
        callback(mic);
    }).catch(function (error) {
        alert('Unable to capture your microphone. Please check console logs.');
        console.error(error);
    });
}
function replaceAudio(src) {
    var newAudio = document.createElement('audio');
    var parentNode = audio.parentNode;
    parentNode.removeChild(audio);
    newAudio.id = "safariAudio";
    newAudio.controls = true;
    newAudio.autoplay = false;
    if (src) {
        newAudio.src = src;
    }
    parentNode.innerHTML = '';
    parentNode.appendChild(newAudio);

    audio = newAudio;
}

function releaseMicrophone() {
    if (microphone) {
        microphone.stop();
        microphone = null;
    }
}

function stopRecordingCallback() {
    replaceAudio(URL.createObjectURL(recorder.getBlob()));
    blob = null;
    blob = recorder.getBlob();
    setTimeout(function () {
        if (!audio.paused) return;
        setTimeout(function () {
            if (!audio.paused) return;
            audio.play();
        }, 1000);

        audio.play();
    }, 300);
    audio.play();

    releaseMicrophone();
}

function click(el) {
    el.disabled = false; // make sure that element is not disabled
    var evt = document.createEvent('Event');
    evt.initEvent('click', true, true);
    el.dispatchEvent(evt);
}

var accepted_legal = false;

var options = {
    fluid: true,
    controls: true,
    width: 600,
    height: 300,
    controlBar: {
        fullscreenToggle: false,
        recordToggle: false
    },
    plugins: {
        wavesurfer: {
            src: 'live',
            waveColor: '#36393b',
            progressColor: 'black',
            debug: false,
            cursorWidth: 1,
            msDisplayMax: 20,
            hideScrollbar: true,
        },
        record: {
            audio: true,
            video: false,
            maxLength: 20,
            debug: false,
            autoMuteDevice: true,
            audioSampleRate: 22050,
            //desiredSampRate: 16000,
            audioChannels: 1,
        },
    }
};
// apply audio workarounds for certain browsers
// applyAudioWorkaround();

if (!isSafari) {
    // other browsers
    createPlayer();
}

function createPlayer(event) {

    player = videojs('myAudio', options, function () {
        // print version information at startup
        var msg = 'Using video.js ' + videojs.VERSION +
            ' with videojs-record ' + videojs.getPluginVersion('record') +
            ', videojs-wavesurfer ' + videojs.getPluginVersion('wavesurfer') +
            ', wavesurfer.js ' + WaveSurfer.VERSION + ' and recordrtc ' +
            RecordRTC.version;
        videojs.log(msg);
    });

    // error handling
    player.on('deviceError', function () {
        console.log('device error:', player.deviceErrorCode);
    });
    player.on('error', function (element, error) {
        console.error(error);
    });
    // user clicked the record button and started recording
    player.on('startRecord', function () {
        console.log('started recording!');
        $('#record-button').text("Stop ");
    });
    // user completed recording and stream is available
    player.on('finishRecord', function () {
        // the blob object contains the recorded data that
        // can be downloaded by the user, stored on server etc.
        console.log('finished recording: ', player.recordedData);
        oldRecording = false;
        $('#record-button').text("Ny optagelse");
    });
}

$('#record-button').on('click', function () {
    if (isSafari) {
        if (typeof recorder === 'undefined' || recorder.getState() === "stopped") {
            if (!microphone) {
                captureMicrophone(function (mic) {
                    microphone = mic;

                    replaceAudio();

                    audio.muted = true;
                    audio.srcObject = microphone;

                    alert('Venligst klik optag igen. Første klik gav adgang til mikrofonen.');
                    return;
                });
                return;
            }
            replaceAudio();

            audio.muted = true;
            audio.srcObject = microphone;

            var options = {
                type: 'audio',
                numberOfAudioChannels: 2,
                checkForInactiveTracks: true,
                desiredSampRate: 22050,
                recorderType: StereoAudioRecorder
            };

            if (recorder) {
                recorder.destroy();
                recorder = null;
            }
            recorder = RecordRTC(microphone, options);

            recorder.startRecording();
            $('#record-button').text("Stop ");

        } else {
            recorder.stopRecording(stopRecordingCallback);
            $('#record-button').text("Ny optagelse ");
        }
    } else {
        if (player.record().isRecording()) {
            player.record().stop();
        } else {
            if (!player.record().stream) {
                alert("Tillad først optagelser ved at klikke på mikrofon ikonet i midten af optagervinduet")
            } else {
                player.record().start();
            }
        }
    }
});

function submitRecording() {
    var hasRecorded = false;
    if (isSafari) {
        if (typeof recorder !== "undefined") {
            hasRecorded = true;
        }
    } else {
        if (player.record().getDuration() !== 0) {
            hasRecorded = true;
        }
    }
    console.log('hasRecorded: ' + hasRecorded);
    console.log('oldRecording: ' + oldRecording);
    console.log('(!hasRecorded || oldRecording)' + (!hasRecorded || oldRecording));
    if (!hasRecorded || oldRecording) {
        alert("Du skal optage sætningen, før du kan sende den ind.")
    } else {
        var mobile_screen = screen.width < 800;
        if (isSafari) {
            var myFile = new File([blob], 'audio.webm');
        } else {
            var myFile = new File([player.recordedData], 'audio.webm');
        }

        var url = "{% url 'save' %}";
        var data = new FormData();
        data.append('recorded_audio', myFile);

        // Add the age from the form to data
        data.append('age', form.age.value);
        data.append('dialect', form.dialect.value);
        data.append('gender', form.gender.value)
        data.append('accent', form.accent.value)
        data.append('zipcode_residence', form.zipcode_residence.value)
        data.append('zipcode_birth', form.zipcode_birth.value)
        data.append('education', form.education.value)
        data.append('occupation', form.occupation.value)
        data.append('transcription', current_trans);
        data.append('ethnicity', form.ethnicity.value);
        data.append('csrfmiddlewaretoken', "{{ csrf_token }}");
        $.ajax({
            url: url,
            method: 'post',
            data: data,
            success: function (data) {
                if (data.success) {
                    alert("Succes! Tak for dit bidrag. Du er velkommen til at sende os flere optagelser!");

                    if (transcriptions.length === 0) {
                        alert("Du har optaget flere end hundrede optagelser. Du er en stjerne!")
                    } else {
                        current_trans = transcriptions.pop();
                        $('#transcription').text(current_trans);
                    }
                }
            },
            error: function () {
                alert("Der gik desværre noget galt. Prøv venligst igen senere.");
            },
            cache: false,
            contentType: false,
            processData: false
        })
        oldRecording = true;
    }
}


var modal = document.getElementById('myModal');

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal

modal.style.display = "block";

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
    modal.style.display = "none";
};

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
};

$('#submitAudio').on('click', function () {
    if (!accepted_legal) {
        modal.style.display = "block";
    } else {
        submitRecording();
    }
});

if (!isSafari) {
    $('#safariAudio').hide();
}

function resetpage() {
    modal.style.display = "none";
    if ($("#accept").prop("checked")) {
        accepted_legal = true;
        if (isSafari) {
            if (typeof recorder !== "undefined") {
                submitRecording();
            }
        } else {
            if (player.record().getDuration() !== 0) {
                submitRecording();
            }
        }

    } else {
        accepted_legal = false;
    }
}
