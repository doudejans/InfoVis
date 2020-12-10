<template>
<div id="sparkline">

</div>
</template>

<script>
import * as d3 from "d3";

export default {
    name: "Sparkline",
    props: {
        width: Number,
        height: Number,
    },
    data() {
        return {
            svg: null,
        }
    },
    mounted() {
        this.initPlot();
    },
    initPlot() {
        const box = d3.select("#sparkline");
        const {width, height} = box.node().getBoundingClientRect();

        this.svg = box.append("svg")
            .attr("width", width)
            .attr("height", height)
            .attr("class", "border");
    }
}
</script>