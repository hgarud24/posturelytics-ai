<template>
  <div>
    <div ref="chartContainer"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import * as Plot from "@observablehq/plot";

const props = defineProps({
  logs: {
    type: Array,
    required: true,
  },
});

const chartContainer = ref(null);

const renderChart = () => {
  if (!props.logs.length) return;

  // const data = props.logs.map((log, i) => ({
  //   time: i,
  //   postureScore: log.posture === 'slouching' ? 0 : 1
  // }))
  console.log("props.log",props.logs)
  const data = props.logs.map((log, i) => ({
    time: i,
    postureScore: log.posture,
    attentionScore: log.attention
  }));

  const goodData = data.filter((d) => d.postureScore === "good");
  const slouchingData = data.filter((d) => d.postureScore === "slouching");
  const focusedData = data.filter((d) => d.attentionScore === "focused");
  const distractedData = data.filter((d) => d.attentionScore === "distracted")

  //console.log("data in observable plot", data);

  const chart = Plot.plot({
    height: 300,
    width: 600,
    y: {
      domain: ["good", "slouching", "focused", "distracted"],
      label: "Posture",
      line: true,
      //tickFormat: d => ('Good', 'Slouching')
    },
    x: {
      label: "Time (index)",
      tickFormat: (d) => `${d}s`,
      line: true,
    },
    marks: [
      Plot.lineY(goodData, {
        x: "time",
        y: "postureScore",
        stroke: "green",
        strokeWidth: 2,
      }),
      Plot.dot(goodData, {
        x: "time",
        y: "postureScore",
        fill: "green",
      }),

      Plot.lineY(slouchingData, {
        x: "time",
        y: "postureScore",
        stroke: "red",
        strokeWidth: 2,
      }),
      Plot.dot(slouchingData, {
        x: "time",
        y: "postureScore",
        fill: "red",
      }),

      Plot.lineY(focusedData, {
        x: "time",
        y: "attentionScore",
        stroke: "blue",
        strokeWidth: 2,
      }),
      Plot.dot(focusedData, {
        x: "time",
        y: "attentionScore",
        fill: "blue",
      }),

      Plot.lineY(distractedData, {
        x: "time",
        y: "attentionScore",
        stroke: "gray",
        strokeWidth: 2,
      }),
      Plot.dot(distractedData, {
        x: "time",
        y: "attentionScore",
        fill: "gray",
      }),
    ],
  });

  chartContainer.value.innerHTML = "";
  chartContainer.value.append(chart);
};

onMounted(renderChart);
watch(() => props.logs, renderChart);
</script>
