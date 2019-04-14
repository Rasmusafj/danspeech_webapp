
transcriptions = [];
{% for transcription in transcriptions %}
    transcriptions.push("{{ transcription }}");
{% endfor %}

var current_trans = transcriptions.pop();
$('#transcription').text(current_trans);

var player;

var accepted_legal = false;

var use_fluid = screen.width < 800;
var options = {
    fluid: use_fluid,
    controls: true,
    width: 600,
    height: 300,
    controlBar: {
        fullscreenToggle: false,
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

if (isSafari) {
    addStartButton();
    var audio = document.querySelector('audio');

    function captureMicrophone(callback) {
        navigator.mediaDevices.getUserMedia({audio: true}).then(callback).catch(function(error) {
            alert('Unable to access your microphone.');
            console.error(error);
        });
    }

    function stopRecordingCallback() {
        audio.srcObject = null;
        var blob = recorder.getBlob();
        audio.src = URL.createObjectURL(blob);
        recorder.microphone.stop();
    }

    document.getElementById('btn-start-recording').onclick = function() {
        this.disabled = true;
        captureMicrophone(function(microphone) {
            audio.srcObject = microphone;
            recorder = RecordRTC(microphone, {
                type: 'audio',
                recorderType: StereoAudioRecorder,
                desiredSampRate: 16000
            });
            recorder.startRecording();
            // release microphone on stopRecording
            recorder.microphone = microphone;
            document.getElementById('btn-stop-recording').disabled = false;
        });
    };
    document.getElementById('btn-stop-recording').onclick = function() {
        this.disabled = true;
        recorder.stopRecording(stopRecordingCallback);
    };
} else {
    // other browsers
    createPlayer();
}
function createPlayer(event) {
    // create player
    if (isSafari) {
        if (event) {
            // hide start button on safari
            event.target.style.display = 'none';
        }
        updateContext(options);
    } else {

    }
    player = videojs('myAudio', options, function() {
        // print version information at startup
        var msg = 'Using video.js ' + videojs.VERSION +
            ' with videojs-record ' + videojs.getPluginVersion('record') +
            ', videojs-wavesurfer ' + videojs.getPluginVersion('wavesurfer') +
            ', wavesurfer.js ' + WaveSurfer.VERSION + ' and recordrtc ' +
            RecordRTC.version;
        videojs.log(msg);
        });

    // error handling
    player.on('deviceError', function() {
        console.log('device error:', player.deviceErrorCode);
    });
    player.on('error', function(element, error) {
        console.error(error);
    });
    // user clicked the record button and started recording
    player.on('startRecord', function() {
        console.log('started recording!');
    });
    // user completed recording and stream is available
    player.on('finishRecord', function() {
        // the blob object contains the recorded data that
        // can be downloaded by the user, stored on server etc.
        console.log('finished recording: ', player.recordedData);
    });
}

$('#submitAudio').on('click', function(){

    if(!accepted_legal){
        modal.style.display = "block";
    } else {
        var myFile = new File([player.recordedData], 'audio.webm');
        var url = "{% url 'save' %}";
        var data = new FormData();
        data.append('recorded_audio', myFile);
        data.append('transcription', current_trans);
        data.append('csrfmiddlewaretoken', "{{ csrf_token }}");
        $.ajax({
            url: url,
            method: 'post',
            data: data,
            success: function(data){
                if(data.success){
                    alert("Sucess! Tak for dit bidrag. Du er velkommen til at sende os flere optagelser!");
                    if (transcriptions.length === 0){
                        alert("You completed 100 recordings! We love you.")
                    }else {
                        current_trans = transcriptions.pop();
                        $('#transcription').text(current_trans);
                    }
                }
            },
            error: function() {
                alert("Something went wrong! Please try again later.");
            },
            cache: false,
            contentType: false,
            processData: false
        });
    }
});


var modal = document.getElementById('myModal');


// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal

modal.style.display = "block";

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
};

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
};


function resetpage() {
    modal.style.display = "none";
    if ($("#accept").prop("checked")){
        accepted_legal = true;
    } else {
        accepted_legal = false;
    }
}
