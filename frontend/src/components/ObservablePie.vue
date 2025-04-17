<template>
    <div ref="chartContainer"></div>
  </template>
  
  <script setup>
  import { ref, onMounted, watch } from 'vue'
  import * as Plot from "@observablehq/plot"
  
  const props = defineProps({
    data: Array,
    title: String
  })
  
  const chartContainer = ref(null)
  
  onMounted(() => {
    renderChart()
  })
  
  watch(() => props.data, () => {
    renderChart()
  })
  
  function renderChart() {
  if (!props.data || !chartContainer.value) return

  console.log("props.data",props.data)

  const chart = Plot.plot({
    width: 300,
    height: 300,
    title: props.title,
    margin: 40,
    marks: [
      Plot.arcY(props.data, {
        x: "label",
        y: "value",
        fill: "label",
        innerRadius: 50,
        outerRadius: 120
      })
    ]
  })

  chartContainer.value.innerHTML = ""
  chartContainer.value.appendChild(chart)
}

  </script>
  