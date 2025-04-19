<template>
    <div class="heatmap-wrapper">
      <svg viewBox="0 0 1536 1024" class="heatmap-svg">
        <image :href="bodyImage" x="0" y="0" width="1536" height="1024" />
        <!-- === BACK VIEW (Right side of SVG) === -->
  
        <!-- TrP1: Neck -->
        <circle
          :cx="triggerPoints.trp1.x"
          :cy="triggerPoints.trp1.y"
          :r="scaleHeat(severity.trp1)"
          fill="red"
          :fill-opacity="opacity(severity.trp1)"
        />
  
        <!-- TrP2: Trapezius Left -->
        <circle
          :cx="triggerPoints.trp2L.x"
          :cy="triggerPoints.trp2L.y"
          :r="scaleHeat(severity.trp2L)"
          fill="red"
          :fill-opacity="opacity(severity.trp2L)"
        />
  
        <!-- TrP2: Trapezius Right -->
        <circle
          :cx="triggerPoints.trp2R.x"
          :cy="triggerPoints.trp2R.y"
          :r="scaleHeat(severity.trp2R)"
          fill="red"
          :fill-opacity="opacity(severity.trp2R)"
        />
  
        <!-- TrP3: Mid-back -->
        <circle
          :cx="triggerPoints.trp3.x"
          :cy="triggerPoints.trp3.y"
          :r="scaleHeat(severity.trp3)"
          fill="red"
          :fill-opacity="opacity(severity.trp3)"
        />
  
        <!-- === FRONT VIEW (Left side of SVG) === -->
  
        <!-- TrP1 Front: Neck -->
        <circle
          :cx="triggerPoints.trp1Front.x"
          :cy="triggerPoints.trp1Front.y"
          :r="scaleHeat(severity.trp1)"
          fill="red"
          :fill-opacity="opacity(severity.trp1)"
        />
  
        <!-- TrP2 Front: Trapezius Left -->
        <circle
          :cx="triggerPoints.trp2LFront.x"
          :cy="triggerPoints.trp2LFront.y"
          :r="scaleHeat(severity.trp2L)"
          fill="red"
          :fill-opacity="opacity(severity.trp2L)"
        />
  
        <!-- TrP2 Front: Trapezius Right -->
        <circle
          :cx="triggerPoints.trp2RFront.x"
          :cy="triggerPoints.trp2RFront.y"
          :r="scaleHeat(severity.trp2R)"
          fill="red"
          :fill-opacity="opacity(severity.trp2R)"
        />
  
        <!-- TrP3 Front: Mid-front -->
        <circle
          :cx="triggerPoints.trp3Front.x"
          :cy="triggerPoints.trp3Front.y"
          :r="scaleHeat(severity.trp3)"
          fill="red"
          :fill-opacity="opacity(severity.trp3)"
        />
      </svg>
    </div>
  </template>
  
  <script setup>
  import { reactive, computed } from "vue";
  import bodyImage from "@/assets/body-outline.svg";
  import { severity } from "../stores/severityStore.js";
  
  // Trigger point coordinates
  // const triggerPoints = {
  //   trp1: { x: 768, y: 200 }, // center-top neck
  //   trp2L: { x: 620, y: 300 }, // left trapezius
  //   trp2R: { x: 920, y: 300 }, // right trapezius
  //   trp3: { x: 768, y: 450 }, // center mid-back
  // };
  
  const triggerPoints = {
    // Back view (right half of SVG, centered at x = 1152)
    trp1:   { x: 1152,       y: 200 }, // center-top back neck
    trp2L:  { x: 1152 - 148, y: 300 }, // left trapezius (back)
    trp2R:  { x: 1152 + 148, y: 300 }, // right trapezius (back)
    trp3:   { x: 1152,       y: 450 }, // center mid-back
  
    // Front view (left half of SVG, centered at x = 384)
    trp1Front:  { x: 384,       y: 200 }, // center-top front neck
    trp2LFront: { x: 384 - 148, y: 300 }, // left trapezius (front)
    trp2RFront: { x: 384 + 148, y: 300 }, // right trapezius (front)
    trp3Front:  { x: 384,       y: 450 }, // center mid-front
  };
  
  
  // Helper functions
  function scaleHeat(val) {
    return 10 + val * 25; // radius from 10 to 35
  }
  function opacity(val) {
    return 0.05 + val * 0.6; // fade from 0.05 to 0.65
  }
  </script>
  
  <style scoped>
  .heatmap-wrapper {
    display: flex;
    justify-content: center;
    margin-top: 2rem;
  }
  .heatmap-svg {
    width: 100%;
    max-width: 700px;
    height: auto;
  }
  </style>