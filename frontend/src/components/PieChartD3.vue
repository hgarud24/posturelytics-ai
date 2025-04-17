<template>
  <div ref="chartContainer"></div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import * as d3 from "d3";

const props = defineProps({
  data: Array,
  title: String,
});

const chartContainer = ref(null);

onMounted(() => {
  renderChart();
});

watch(
  () => props.data,
  () => {
    renderChart();
  }
);

function renderChart() {
  const data = props.data;
  const width = 300;
  const height = 300;

  const color = d3
    .scaleOrdinal()
    .domain(data.map((d) => d.label))
    .range(
      d3
        .quantize((t) => d3.interpolateSpectral(t * 0.8 + 0.1), data.length)
        .reverse()
    );

  const pie = d3
    .pie()
    .sort(null)
    .value((d) => d.value);

  const arc = d3
    .arc()
    .innerRadius(0)
    .outerRadius(Math.min(width, height) / 2 - 1);

  const labelRadius = arc.outerRadius()() * 0.8;

  const arcLabel = d3.arc().innerRadius(labelRadius).outerRadius(labelRadius);

  const arcs = pie(data);

  const svg = d3
    .create("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", [-width / 2, -height / 2, width, height])
    .attr("style", "max-width:100%; height:auto; font: 10px sans-serif;");

  svg
    .append("g")
    .attr("stroke", "white")
    .selectAll("path")
    .data(arcs)
    .join("path")
    .attr("fill", (d) => color(d.data.label))
    .attr("d", arc)
    .append("title")
    .text((d) => `${d.data.label}: ${d.data.value.toLocaleString("en-US")}`);

  svg
    .append("g")
    .attr("text-anchor", "middle")
    .selectAll("text")
    .data(arcs)
    .join("text")
    .attr("transform", (d) => `translate(${arcLabel.centroid(d)})`)
    .call((text) =>
      text
        .append("tspan")
        .attr("y", "-0.4em")
        .attr("font-weight", "bold")
        .text((d) => d.data.label)
    )
    .call((text) =>
      text
        .filter((d) => d.endAngle - d.startAngle > 0.25)
        .append("tspan")
        .attr("x", 0)
        .attr("y", "0.7em")
        .attr("fill-opacity", 0.7)
        .text((d) => d.data.value.toLocaleString("en-US"))
    );

  chartContainer.value.innerHTML = ""; // Clear previous chart if any
  chartContainer.value.appendChild(svg.node());
}
</script>
