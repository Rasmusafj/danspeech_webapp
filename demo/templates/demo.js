
var player;
var recorder;
var microphone;
var blob;

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

function createPlayer(event) {

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
        $('#record-button').text("Stop ");
    });
    // user completed recording and stream is available
    player.on('finishRecord', function() {
        // the blob object contains the recorded data that
        // can be downloaded by the user, stored on server etc.
        console.log('finished recording: ', player.recordedData);
        $('#record-button').text("Ny optagelse");
        sendAudio();
    });
}

$('#record-button').on('click', function(){
    if (player.record().isRecording()) {
        player.record().stop();
    } else {
        if (!player.record().stream){
            alert("Tillad først optagelser ved at klikke på mikrofon ikonet i midten af optagervinduet")
        } else {
            player.record().start();
        }
    }

});

$('#submitAudio').on('click', function(){
    transcribe();
});

function transcribe() {
    alert("Not implemented yet...");
}


function sendAudio(){
    var hasRecorded = false;
    if (player.record().getDuration() !== 0){
        hasRecorded = true;
    }

    if (!hasRecorded){
        alert("Du skal optage en sætning")
    } else {
        var url = "{% url 'preprocess_audio' %}";
        var data = new FormData();
        var myFile = new File([player.recordedData], 'audio.webm');
        data.append('recorded_audio', myFile);
        data.append('csrfmiddlewaretoken', "{{ csrf_token }}");
        $.ajax({
            url: url,
            method: 'post',
            data: data,
            success: function(data){

            },
            error: function() {
                alert("Der gik desværre noget galt. Prøv venligst igen.");
            },
            cache: false,
            contentType: false,
            processData: false
        });
    }
}

createPlayer();
