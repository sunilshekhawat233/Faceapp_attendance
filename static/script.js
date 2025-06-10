const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureBtn = document.getElementById('captureBtn');
const webcamForm = document.getElementById('webcamForm');
const webcamImageInput = document.getElementById('webcamImageInput');

// Access webcam
navigator.mediaDevices.getUserMedia({ video: true })
  .then((stream) => {
    video.srcObject = stream;
  })
  .catch((err) => {
    alert("Webcam not available.");
    console.error(err);
  });

// Capture image
captureBtn.addEventListener('click', () => {
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext('2d').drawImage(video, 0, 0);
  const dataURL = canvas.toDataURL('image/png');
  webcamImageInput.value = dataURL;
  webcamForm.style.display = 'block';
});
