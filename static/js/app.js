const video = document.querySelector('video');
const canvas = document.querySelector('canvas');
const capture = document.querySelector('button');
const traduccion = document.querySelector('#traduccion');
const synth = window.speechSynthesis;
let socket = io();
let cameraReady = false;
let cameraOptions = 'none';
let streamStarted = false;
let streamRunning = false;
let facingMode = "environment";
//let facingMode = "user";

const videoWidth = 832 ; 
const videoHeight = 68 ; 

canvas.hidden = true;
canvas.width = videoWidth;
canvas.height = videoHeight;
let ctx = canvas.getContext('2d');

const constraints = {
  video: {
    width:  {
      ideal: videoWidth,
            },
    height: {
      ideal: videoHeight,
            },
    facingMode: facingMode
        },
  audio: false,
                    };


capture.onclick = function() {
capture.disabled = true;
video.pause();
ctx.drawImage(video, 0, 0, canvas.width, canvas.height );
imageData = canvas.toDataURL('image/jpeg');
socket.emit("traducir", JSON.stringify({imageData: imageData}));
traduccion.textContent = "Traduciendo texto...";
socket.once('traducido', function (traducc) {
traduccion.textContent = traducc;
const utterThis = new SpeechSynthesisUtterance(traducc);
utterThis.lang = 'es-ES';
utterThis.rate = 0.8;
synth.speak(utterThis);
video.play();
capture.disabled = false; 
                                            });
                                };

                       
const startStream = async (constraints) => {
  const stream = await navigator.mediaDevices.getUserMedia(constraints);
  handleStream(stream);
                                            };

const handleStream = (stream) => {
  video.srcObject = stream;
  streamStarted = true;
                                  };

const getCameraSelection = async () => {
  const devices = await navigator.mediaDevices.enumerateDevices();
  const videoDevices = devices.filter(device => device.kind === 'videoinput');
  if (videoDevices.length === 0) {
                                  return;
                                  }
  const options = videoDevices.map(videoDevice => {
    return `<option value="${videoDevice.deviceId}">${videoDevice.label}</option>`;
                                                  });
  cameraOptions = options.join('');
  cameraReady = true;
                                        };

(function waitCamera() {
  getCameraSelection();
  if(cameraReady == false) {
    setTimeout(waitCamera, 500 );
                            }
                        })
();


if ('mediaDevices' in navigator && navigator.mediaDevices.getUserMedia) {   
  const updatedConstraints = {
    ...constraints,
    deviceId: {
              exact: cameraOptions
              },
                              };
  updatedConstraints.video.facingMode = facingMode;
  startStream(updatedConstraints);
                                                                        }
video.play();
streamRunning = true;