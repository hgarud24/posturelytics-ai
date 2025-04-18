<template>
  <div style="text-align: center; padding: 2rem">
    <h2>Focus Session</h2>

    <div v-if="!sessionActive">
      <label for="duration">Select Duration (in minutes):</label>
      <input
        id="duration"
        type="number"
        min="1"
        max="180"
        v-model="sessionDurationMinutes"
      />
      <button @click="startSession">Start Session</button>
    </div>

    <div v-else>
      <h3>Time Left: {{ formatTime(timeLeft) }}</h3>
      <button @click="endSession">End Session</button>
    </div>
    <div v-if="sessionComplete">
      <h2>Session Summary</h2>
      <div class="feedback-box">
        <h3>AI Feedback</h3>
        <p>{{ gptFeedback }}</p>
      </div>

      <!-- <ObservablePie :data="focusStats" title="Focus vs Distraction" />
      <ObservablePie :data="postureStats" title="Posture Quality" /> -->
      <!-- Add more charts if needed -->
      <PieChartD3 :data="focusStats" title="Focus vs Distraction" />
      <PieChartD3 :data="postureStats" title="Posture Quality" />
      <PostureLineChart :logs="sessionLogs" />
    </div>

    <PoseTracker v-if="sessionActive" @status-update="handleStatusUpdate" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import PoseTracker from "../components/PoseTracker.vue";
import PostureLineChart from "../components/ObservableLinechart.vue";
import PieChartD3 from "../components/PieChartD3.vue";
import axios from "axios";

const sessionActive = ref(false);
const sessionDuration = ref(0); // seconds
const timeLeft = ref(0);
const sessionDurationMinutes = ref(25); // default duration
const sessionLogs = ref([]);
let timerInterval = null;
const sessionComplete = ref(false);
const gptFeedback = ref("");

// const token = localStorage.getItem('token')

function handleStatusUpdate(data) {
  if (sessionActive.value) {
    sessionLogs.value.push(data);
    console.log("sessionLogs", sessionLogs);
  }
}

function startSession() {
  sessionDuration.value = sessionDurationMinutes.value * 60;
  timeLeft.value = sessionDuration.value;
  sessionLogs.value = [];

  sessionActive.value = true;

  timerInterval = setInterval(() => {
    if (timeLeft.value > 0) {
      timeLeft.value--;
    } else {
      endSession();
    }
  }, 1000);
}

function formatTime(seconds) {
  const m = Math.floor(seconds / 60)
    .toString()
    .padStart(2, "0");
  const s = (seconds % 60).toString().padStart(2, "0");
  return `${m}:${s}`;
}

function speak(text) {
  const synth = window.speechSynthesis;
  const utterance = new SpeechSynthesisUtterance(text);
  synth.speak(utterance);
}

async function endSession() {
  sessionActive.value = false;
  sessionComplete.value = true;
  clearInterval(timerInterval);
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

  // Debug log
  console.log("Session Summary:");
  console.log(`Duration: ${sessionDuration.value / 60} minutes`);
  console.log(`Total Logs Collected: ${sessionLogs.value.length}`);
  console.log("Sample Log:", sessionLogs.value.slice(0, 5));

  const token = localStorage.getItem("token");

  try {
    await axios.post("http://127.0.0.1:8000/api/session", sessionData, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    console.log("Session saved");
  } catch (err) {
    console.error("Failed to save session:", err);
  }

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
button {
  margin-top: 1rem;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}
input {
  margin-left: 10px;
  width: 60px;
  padding: 5px;
}
.feedback-box {
  background: #f5f5f5;
  border-left: 6px solid #4caf50;
  padding: 1rem;
  margin-top: 1.5rem;
  font-style: italic;
  border-radius: 6px;
}
</style>
