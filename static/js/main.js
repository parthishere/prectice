console.log("ok");
var video1, video2,button;
var connect=false;

var loc = window.location;

var endPoint = '';
var wsStart = 'ws://';

if(loc.protocol == 'https:'){
    wsStart = 'wss://';
}

var endPoint = wsStart + loc.host + loc.pathname;

var ws = new WebSocket(endPoint);
ws.onopen = function(e) {
    connect=true;
};
video1=document.querySelector('#video1');
button=document.querySelector("#btn");
console.log(button)

ws.binaryType = 'arraybuffer';
navigator.mediaDevices.getUserMedia({ video: {width: 400, height: 400}})
    .then(stream => {
        var streamChunks = [];
        var outChunks = [];
        var binaryData = [];
        binaryData.push(stream);
        
        video1.srcObject = stream
        console.log("before sending")
        
        if(connect==true){
            // streamChunks.push(event.data);
            ws.send(stream.data );
            console.log(stream);
        }
});

var mediaSource = new MediaSource();
var buffer;
var queue = [];
video2=document.querySelector('#video2');

mediaSource.addEventListener('sourceopen', function(e) {
    video2.play();
    buffer = mediaSource.addSourceBuffer('video/webm; codecs="vorbis,vp8"');

    buffer.addEventListener('update', function() { //Note: Have tried 'updateend'
        if (queue.length > 0 && !buffer.updating) {
            buffer.appendBuffer(queue.shift());
        }
    });
}, false);
video2.src=window.URL.createObjectURL(mediaSource);
ws.onmessage = function(event) {
    console.log(event.data)
    if (event.data instanceof ArrayBuffer) {
        try {
           if (buffer.updating || queue.length > 0) {
            queue.push(event.data);
           } else {
            buffer.appendBuffer(event.data);
           }
        }  catch (e) {
            console.log(e);
        }                               
}  else  {
    writeResponse(event.data); 
}
};
// </script>


// webSocket.onopen = function(e){
//     console.log('Connection opened! ', e);
// }

// webSocket.onmessage = function(e){
//     console.log('message! ', e);
// }

// webSocket.onclose = function(e){
//     console.log('Connection closed! ', e);
// }

// webSocket.onerror = function(e){
//     console.log('Error occured! ', e);
// }