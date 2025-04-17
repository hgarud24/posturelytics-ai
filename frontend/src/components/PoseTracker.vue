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

// function calculatePostureScore(landmarks) {
//   const leftShoulder = landmarks[11];
//   const rightShoulder = landmarks[12];
//   const leftHip = landmarks[23];
//   const rightHip = landmarks[24];

//   const avgShoulderY = (leftShoulder.y + rightShoulder.y) / 2;
//   const avgHipY = (leftHip.y + rightHip.y) / 2;

//   const deltaY = avgHipY - avgShoulderY;
//   return deltaY > 0.15 ? "slouching" : "good";
// }

function calculatePostureScore(landmarks) {
  if (!landmarks || landmarks.length < 25) return "unknown"

  const leftShoulder = landmarks[11]
  const rightShoulder = landmarks[12]
  const leftHip = landmarks[23]
  const rightHip = landmarks[24]

  // Midpoints of shoulders and hips
  const midShoulder = {
    x: (leftShoulder.x + rightShoulder.x) / 2,
    y: (leftShoulder.y + rightShoulder.y) / 2,
    z: (leftShoulder.z + rightShoulder.z) / 2,
  }
  const midHip = {
    x: (leftHip.x + rightHip.x) / 2,
    y: (leftHip.y + rightHip.y) / 2,
    z: (leftHip.z + rightHip.z) / 2,
  }

  // Slope of vector (for side leaning)
  const dx = midHip.x - midShoulder.x
  const dy = midHip.y - midShoulder.y
  const dz = midHip.z - midShoulder.z

  // Side angle: horizontal lean (X-axis)
  const sideAngleDeg = Math.atan2(dx, dy) * (180 / Math.PI)

  // Forward slouch detection using depth (Z-axis)
  const zSlouchThreshold = -0.1
  const zDifference = midShoulder.z - midHip.z

  const isSideLeaning = Math.abs(sideAngleDeg) > 1   // side tilt threshold
  const isForwardSlouching = zDifference < zSlouchThreshold  // slouched forward
  console.log("Z diff:", zDifference.toFixed(3), "Side angle:", sideAngleDeg.toFixed(2))

  if (isSideLeaning || isForwardSlouching) {
    return "slouching"
  } else {
    return "good"
  }
  // < -0.2 - then slouch
}


function isLookingAway(landmarks) {
  if (!landmarks || landmarks.length < 468) return false;

  const leftEye = landmarks[33]; // outer corner of left eye
  const rightEye = landmarks[263]; // outer corner of right eye
  const nose = landmarks[1];

  const eyeMidX = (leftEye.x + rightEye.x) / 2;
  const deviation = Math.abs(eyeMidX - nose.x); // how centered is the nose?

  // Lower value = looking straight; higher = head turned
  return deviation > 0.06; // tune threshold, 0.05–0.07 often works
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
  faceMesh.onResults((results) => {
    if (results.multiFaceLandmarks) {
      const face = results.multiFaceLandmarks[0];
      const away = isLookingAway(face);
      console.log("Attention:", away ? "Away" : "Focused");

      if (away) {
        zoneOutCount++;
        if (zoneOutCount >= 5 && !isLookingAwaySpoken) {
          speak("You're looking away. Please refocus.");
          isLookingAwaySpoken = true;
          zoneOutCount = 0;
        }
      } else {
        zoneOutCount = 0;
        isLookingAwaySpoken = false; // reset flag when focused again
      }
    }
  });

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
