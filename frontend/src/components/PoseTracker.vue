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
import { Camera } from "../utils/camera_utils.js";
import { FaceMesh } from "@mediapipe/face_mesh";
import { defineEmits } from "vue";
import { severity } from "../stores/severityStore.js"


const emit = defineEmits(["status-update"]);

const video = ref(null);
const canvas = ref(null);

let camera = null;
let zoneOutCount = 0;
let isLookingAwaySpoken = false;

let latestPosture = "unknown";
let latestAttention = "unknown";
let cameraRunning = true;

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

  const forwardZ = nose.z - avgShoulder.z;
  const verticalDrop = nose.y - avgShoulder.y;

  const isForwardHead = forwardZ < -0.9;
  const isHeadDropped = verticalDrop > -0.2;

  return isForwardHead || isHeadDropped ? "slouching" : "good";
}

function isLookingAway(landmarks) {
  if (!landmarks || landmarks.length < 468) return false;

  const leftEye = landmarks[33];
  const rightEye = landmarks[263];
  const nose = landmarks[1];
  const chin = landmarks[152];
  const forehead = landmarks[10];

  const eyeMidX = (leftEye.x + rightEye.x) / 2;
  const deviationSide = Math.abs(eyeMidX - nose.x);

  const verticalDistance = Math.abs(chin.y - forehead.y);
  const dx = chin.x - forehead.x;
  const dy = chin.y - forehead.y;
  const deviationUpDown = Math.atan2(dy, dx) * (180 / Math.PI);

  const isDeviation =
    deviationSide > 0.01 || (deviationUpDown > 90 && verticalDistance < 0.25);

  return isDeviation;
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
      latestPosture = calculatePostureScore(results.poseLandmarks);
    }
  });

  faceMesh.onResults((results) => {
    if (results.multiFaceLandmarks) {
      const face = results.multiFaceLandmarks[0];
      const isZonedOut = isLookingAway(face);

      latestAttention = isZonedOut ? "distracted" : "focused";

      if (isZonedOut) {
        zoneOutCount++;
        if (zoneOutCount > 5 && !isLookingAwaySpoken) {
          speak("You're looking away. Please refocus.");
          isLookingAwaySpoken = true;
          zoneOutCount = 0;
        }
      } else {
        zoneOutCount = 0;
        isLookingAwaySpoken = false;
      }
    } else {
      latestAttention = "absent";
    }
  });

  camera = new Camera(video.value, {
    onFrame: async () => {
      if (!cameraRunning) return;

      await pose.send({ image: video.value });
      await faceMesh.send({ image: video.value });

      if (latestPosture === "slouching") {
        severity.trp1 = Math.min(1.0, severity.trp1 + 0.05);
        severity.trp2L = Math.min(1.0, severity.trp2L + 0.05);
        severity.trp2R = Math.min(1.0, severity.trp2R + 0.05);
        severity.trp3 = Math.min(1.0, severity.trp3 + 0.03);
      } else if (latestPosture === "good") {
        severity.trp1 = Math.max(0, severity.trp1 - 0.01);
        severity.trp2L = Math.max(0, severity.trp2L - 0.01);
        severity.trp2R = Math.max(0, severity.trp2R - 0.01);
        severity.trp3 = Math.max(0, severity.trp3 - 0.01);
      }

      emit("status-update", {
        timestamp: new Date().toISOString(),
        posture: latestPosture,
        attention: latestAttention,
      });
    },
    width: 640,
    height: 480,
  });

  camera.start();
});

onUnmounted(() => {
  cameraRunning = false;

  if (video.value && video.value.srcObject) {
    const tracks = video.value.srcObject.getTracks();
    tracks.forEach((track) => track.stop());
    video.value.srcObject = null;
  }

  window.speechSynthesis.cancel();

  if (camera && camera.stop) {
    camera.stop();
  }
});
</script>
