<template>
  <div>
    <video
      ref="video"
      autoplay
      playsinline
      muted
      width="640"
      height="480"
    ></video>
    <canvas ref="canvas" width="640" height="480"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { Pose } from "@mediapipe/pose";
import { Camera } from "../utils/camera_utils.js"; // make sure path is correct
import { FaceMesh } from "@mediapipe/face_mesh";

const video = ref(null);
const canvas = ref(null);
let camera = null;
let zoneOutCount = 0;
let isLookingAwaySpoken = false;
let isUserGoneSpoken = false;

function speak(text) {
  const synth = window.speechSynthesis;
  const utterance = new SpeechSynthesisUtterance(text);
  synth.speak(utterance);
}

function calculatePostureScore(landmarks) {
  if (!landmarks || landmarks.length < 13) return "unknown";

  const nose = landmarks[0];
  const leftShoulder = landmarks[11];
  const rightShoulder = landmarks[12];

  const avgShoulder = {
    x: (leftShoulder.x + rightShoulder.x) / 2,
    y: (leftShoulder.y + rightShoulder.y) / 2,
    z: (leftShoulder.z + rightShoulder.z) / 2,
  };

  // Forward head posture detection (nose in front of shoulders)
  const forwardZ = nose.z - avgShoulder.z;

  // Head tilt detection (neck strain)
  const verticalDrop = nose.y - avgShoulder.y;

  // Logging for debug
  console.log(
    "Z forward lean:", forwardZ.toFixed(3),
    "Vertical drop:", verticalDrop.toFixed(3)
  );

  const isForwardHead = forwardZ < -0.9;      // more negative = forward
  const isHeadDropped = verticalDrop > -0.20;   // head lower than shoulder

  if (isForwardHead || isHeadDropped) {
    return "slouching";
  } else {
    return "good";
  }
}

function isLookingAway(landmarks) {
  if (!landmarks || landmarks.length < 468) return false;

  const leftEye = landmarks[33]; // outer corner of left eye
  const rightEye = landmarks[263]; // outer corner of right eye
  const nose = landmarks[1];
  const chin=landmarks[152];
  const forehead=landmarks[10];

  const eyeMidX = (leftEye.x + rightEye.x) / 2;
  const deviationSide = Math.abs(eyeMidX - nose.x); // how centered is the nose?


  const verticalDistance = Math.abs(chin.y-forehead.y);

  const dx = chin.x - forehead.x;
  const dy = chin.y - forehead.y;

  const deviationUpDown = Math.atan2(dy,dx) * (180/Math.PI);
  console.log("deviationUpDown",deviationUpDown);
  console.log("verticalDistance",verticalDistance);

  const isDeviation = (deviationSide > 0.01) || (deviationUpDown > 90 && verticalDistance < 0.25);

  console.log(isDeviation);
 
  return isDeviation 
}

onMounted(() => {
  const pose = new Pose({
    locateFile: (file) =>
      `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`,
  });
  pose.setOptions({
    modelComplexity: 1,
    smoothLandmarks: true,
    enableSegmentation: false,
    minDetectionConfidence: 0.5,
    minTrackingConfidence: 0.5,
  });

  const faceMesh = new FaceMesh({
    locateFile: (file) =>
      `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${file}`,
  });
  faceMesh.setOptions({
    maxNumFaces: 1,
    refineLandmarks: true,
    minDetectionConfidence: 0.5,
    minTrackingConfidence: 0.5,
  });

  pose.onResults((results) => {
    const ctx = canvas.value.getContext("2d");
    ctx.clearRect(0, 0, canvas.value.width, canvas.value.height);
    ctx.drawImage(results.image, 0, 0, canvas.value.width, canvas.value.height);

    if (results.poseLandmarks) {
      const postureStatus = calculatePostureScore(results.poseLandmarks);
      console.log("Posture:", postureStatus);
    }
  });
  // faceMesh.onResults((results) => {
  //   if (results.multiFaceLandmarks) {
  //     const face = results.multiFaceLandmarks[0];
  //     const away = isLookingAway(face);
  //     console.log("Attention:", away ? "Away" : "Focused");

  //     if (away) {
  //       zoneOutCount++;
  //       if (zoneOutCount >= 5 && !isLookingAwaySpoken) {
  //         speak("You're looking away. Please refocus.");
  //         isLookingAwaySpoken = true;
  //         zoneOutCount = 0;
  //       }
  //     } else {
  //       zoneOutCount = 0;
  //       isLookingAwaySpoken = false; // reset flag when focused again
  //     }
  //   }
  // });

  faceMesh.onResults((results) =>{
    if (results.multiFaceLandmarks) {
    const face = results.multiFaceLandmarks[0];
    const isZonedOut = isLookingAway(face);

      if(isZonedOut){
        zoneOutCount++;
        if(zoneOutCount >5 && !isLookingAwaySpoken){
          speak("You're looking away. Please refocus.");
          isLookingAwaySpoken = true;
          zoneOutCount = 0;
        }
      }
      else{
        zoneOutCount = 0;
        isLookingAwaySpoken = false;
      }
  }})

  camera = new Camera(video.value, {
    onFrame: async () => {
      await pose.send({ image: video.value });
      await faceMesh.send({ image: video.value });
    },
    width: 640,
    height: 480,
  });

  camera.start();
});

onUnmounted(() => {
  console.log("Cleaning up camera and speech...")

  // Stop camera stream
  if (video.value && video.value.srcObject) {
    const tracks = video.value.srcObject.getTracks()
    tracks.forEach(track => track.stop())
    video.value.srcObject = null
  }

  // Stop any ongoing speech synthesis
  window.speechSynthesis.cancel()

  // Optional: Stop camera processing loop if needed
  if (camera && camera.stop) {
    camera.stop()
  }
});
</script>
