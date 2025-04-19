<template>
  <div class="focus-container">
    <h1 class="title">Welcome to Posturelytics AI</h1>
    <p class="tagline">Elevate Your Posture,<br />Boost Your Productivity</p>

    <!-- START SESSION SCREEN -->
    <div
      v-if="!sessionActive && !sessionComplete && !showAnalytics"
      class="start-box"
    >
      <label for="duration">Set Time (minutes):</label>
      <input
        id="duration"
        type="number"
        min="1"
        max="180"
        v-model="sessionDurationMinutes"
      />
      <button class="start-btn" @click="startSession">Start Session</button>
    </div>

    <div
      v-if="!sessionActive && !sessionComplete && !showAnalytics"
      class="illustration-row"
    >
      <img
        src="@/assets/sitting-illustration.png"
        alt="Sitting Posture"
        class="illustration"
      />
      <img
        src="@/assets/analytics-illustration.png"
        alt="Analytics"
        class="illustration"
      />
    </div>

    <!-- ACTIVE SESSION -->
    <div v-if="sessionActive" class="active-session">
      <h3>Time Left: {{ formatTime(timeLeft) }}</h3>
      <PoseTracker @status-update="handleStatusUpdate" />
      <button class="end-btn" @click="endSession">End Session</button>
    </div>

    <!-- POST SESSION CONTROLS (Always show after session ends) -->
    <div v-if="sessionComplete" class="post-session-options">
      <label for="duration">Set Time (minutes):</label>
      <input
        id="duration"
        type="number"
        min="1"
        max="180"
        v-model="sessionDurationMinutes"
      />
      <button class="start-btn" @click="startSession">Start Session</button>
      <button class="analytics-btn" @click="showAnalytics = true">
        View Analytics
      </button>
    </div>

    <!-- ANALYTICS (conditionally shown on toggle) -->
    <div v-if="showAnalytics" class="analytics-view">
      <h2>Session Summary</h2>
      <div class="feedback-box">
        <h3>AI Feedback</h3>
        <p>{{ gptFeedback }}</p>
      </div>
      <div class="chart-row">
        <PieChartD3 :data="focusStats" title="Focus vs Distraction" />
        <PieChartD3 :data="postureStats" title="Posture Quality" />
      </div>

      <PostureLineChart :logs="sessionLogs" />

     <!--This logic is for rendering the posture heat map-->
     <PostureHeatmap />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import PoseTracker from "../components/PoseTracker.vue";
import PostureLineChart from "../components/ObservableLinechart.vue";
import PieChartD3 from "../components/PieChartD3.vue";
import axios from "axios";
import PostureHeatmap from '../components/PostureHeatmap.vue';

const sessionActive = ref(false);
const sessionComplete = ref(false);
const showAnalytics = ref(false);
const sessionDuration = ref(0);
const timeLeft = ref(0);
const sessionDurationMinutes = ref(25);
const sessionLogs = ref([]);
const gptFeedback = ref("");
let timerInterval = null;

function handleStatusUpdate(data) {
  if (sessionActive.value) {
    sessionLogs.value.push(data);
  }
}

function startSession() {
  sessionDuration.value = sessionDurationMinutes.value * 60;
  timeLeft.value = sessionDuration.value;
  sessionLogs.value = [];
  gptFeedback.value = "";
  showAnalytics.value = false;
  sessionActive.value = true;
  sessionComplete.value = false;

  timerInterval = setInterval(() => {
    if (timeLeft.value > 0) {
      timeLeft.value--;
    } else {
      endSession();
    }
  }, 1000);
}

function speak(text) {
  const synth = window.speechSynthesis;
  const utterance = new SpeechSynthesisUtterance(text);
  synth.speak(utterance);
}

async function endSession() {
  clearInterval(timerInterval);
  sessionActive.value = false;
  sessionComplete.value = true;
  speak("Focus session complete. Great job!");

  const sessionData = {
    userId: "anonymous",
    duration: sessionDuration.value,
    logs: sessionLogs.value,
    startedAt: new Date(
      Date.now() - sessionDuration.value * 1000
    ).toISOString(),
    endedAt: new Date().toISOString(),
  };

  const token = localStorage.getItem("token");

  try {
    const res = await axios.post(
      "http://127.0.0.1:8000/api/session",
      sessionData,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    console.log("Session saved");
    gptFeedback.value = res.data.feedback || "No feedback received.";
  } catch (err) {
    console.error("Failed to save session:", err);
    gptFeedback.value = "Session saved locally, but feedback failed.";
  }
}

function formatTime(seconds) {
  const m = Math.floor(seconds / 60)
    .toString()
    .padStart(2, "0");
  const s = (seconds % 60).toString().padStart(2, "0");
  return `${m}:${s}`;
}

const focusStats = computed(() => {
  const focused = sessionLogs.value.filter(
    (l) => l.attention === "focused"
  ).length;
  const distracted = sessionLogs.value.length - focused;

  return [
    { label: "Focused", value: focused },
    { label: "Distracted", value: distracted },
  ];
});

const postureStats = computed(() => {
  const good = sessionLogs.value.filter((l) => l.posture === "good").length;
  const slouch = sessionLogs.value.length - good;

  return [
    { label: "Good", value: good },
    { label: "Slouching", value: slouch },
  ];
});
</script>

<style scoped>
/* .title{
  font-size: xxx-large;
  font-family: 'Arial' sans-serif !important;
} */
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap");
.focus-container {
  text-align: center;
  padding: 2rem;
  color: #fff;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #010d2d;
  flex-direction: column;
}

h1 {
  font-size: 4rem;
  margin-bottom: 0.5rem;
  font-family: "Inter";
  color: #dcdcdc;
}

.tagline {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  color: #ccc;
}

.start-box,
.post-session-options {
  margin-top: 2rem;
}

.analytics-view {
  margin-top: 3rem;
  background: #222;
  border-radius: 10px;
  padding: 1.5rem;
  box-shadow: 0 0 10px #000;
}

button {
  margin: 0.5rem;
  padding: 12px 24px;
  font-size: 16px;
  font-weight: 500;
  border-radius: 8px;
  cursor: pointer;
  border: none;
  transition: 0.2s;
}

.start-btn {
  background-color: #00bfa5;
  color: white;
}
.analytics-btn {
  background-color: #eeeeee;
  color: black;
}
.end-btn {
  background-color: #ef5350;
  color: white;
}

.feedback-box {
  background: #f5f5f5;
  border-left: 6px solid #4caf50;
  color: #333;
  padding: 1rem;
  margin-top: 1.5rem;
  font-style: italic;
  border-radius: 6px;
}
input {
  padding: 0.5rem;
  width: 70px;
  margin-left: 0.5rem;
  border-radius: 5px;
  border: 1px solid #ccc;
  background-color: #fff;
  color: #000;
  font-weight: 500;
  text-align: center;
}
.illustration-row {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 2rem;
  flex-wrap: wrap;
}

.illustration {
  width: 400px;
  height: auto;
  border-radius: 8px;
}

.chart-row {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 2rem;
  margin-bottom: 2rem;
  margin-top:2rem;
}

.chart-row > * {
  flex: 1 1 300px;
  max-width: 400px;
}

</style>
