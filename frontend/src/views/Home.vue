<template>
  <v-app>
    <!-- Hero Section -->
    <div class="hero-section py-16">
      <v-row align="center" justify="space-between">
        <v-col cols="12" md="6">
          <h1 class="text-h4 font-weight-bold mb-4">
            Your AI Posture & Productivity Coach
          </h1>
          <p class="mb-6">
            Monitor your posture and stay productive in real-time with
            AI-powered insights.
          </p>
          <v-btn color="primary" to="/login" large class="white--text">Get Started</v-btn>
        </v-col>
        <v-col cols="12" md="6">
          <img
            src="../assets/illustration-posture.png"
            alt="Posture Illustration"
            max-width="450"
            class="mx-auto image-card"
          />
        </v-col>
      </v-row>
    </div>

    <!-- Features Section -->
    <div class="features-section py-12" fluid>
      <h2 class="text-center text-h5 font-weight-bold mb-8">Features</h2>
      <v-row justify="center" class="text-center">
        <v-col cols="12" sm="4">
          <v-card flat class="pa-6 feature-card">
            <v-icon color="cyan" size="40">mdi-human-male-height</v-icon>
            <h3 class="mt-3 font-weight-medium">Live Posture Detection</h3>
            <p class="mt-2">
              Continuous monitoring to ensure productivity and posture health.
            </p>
          </v-card>
        </v-col>
        <v-col cols="12" sm="4">
          <v-card flat class="pa-6 feature-card">
            <v-icon color="cyan" size="40">mdi-timer-outline</v-icon>
            <h3 class="mt-3 font-weight-medium">Focus Timer</h3>
            <p class="mt-2">
              Stay consistent with posture-locked productivity sessions.
            </p>
          </v-card>
        </v-col>
        <v-col cols="12" sm="4">
          <v-card flat class="pa-6 feature-card">
            <v-icon color="cyan" size="40">mdi-chart-bar</v-icon>
            <h3 class="mt-3 font-weight-medium">Posture Summary</h3>
            <p class="mt-2">
              Analyze session-wise posture reports and performance.
            </p>
          </v-card>
        </v-col>
      </v-row>
    </div>

    <!-- Live Demo Section -->
    <div class="live-demo-section py-16 text-center">
      <v-row align="center" justify="space-between">
        <v-col cols="12" md="6">
          <h2 class="text-h5 font-weight-bold mb-4">Live Demo</h2>
          <p>See your posture in real time with our webcam analysis</p>
        </v-col>
        <v-col>
          <img
            src="../assets/live-demo-placeholder.png"
            alt="Live Posture Detection Preview"
            max-width="500"
            class="mx-auto mt-6 image-card"

          />
        </v-col>
      </v-row>
    </div>
  </v-app>
</template>

<script setup>
// no logic needed yet
</script>

<style scoped>
.hero-section {
  background-color: #010d2d;
  color: white;
  padding-left: 50px;
}
.features-section {
  background-color: #010d2d;
  color: white;
  padding-left: 50px;
}
.live-demo-section {
  background-color: #010d2d;
  color: white;
}
.feature-card {
  background-color: #1e2e4d;
  border-radius: 12px;
  color: white;
  width: 400px;
}
.image-card {
  width: 500px;
  height: 500px;
}
</style>
