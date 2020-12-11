<template>
<div id="sparkline">

</div>
</template>

<script>
import * as d3 from "d3";

export default {
    name: "Sparkline",
    props: {
        data: Array
    },
    data() {
        return {
            svg: null,
            width: 0,
            height: 0,
            padding: 10,
        }
    },
    mounted() {
        this.initPlot();
        this.drawLine();
    },
    methods: {
        initPlot() {
            const box = d3.select("#sparkline");
            const {width, height} = box.node().getBoundingClientRect();
            this.width = width;
            this.height = height;

            this.svg = box.append("svg")
                .attr("width", width)
                .attr("height", height)
                .attr("class", "");
        },
        drawLine() {
            const xScale = d3.scaleTime()
                .domain([new Date("2011"), new Date("2019")])
                .range([0 + this.padding, this.width - this.padding]);

            const yScale = d3.scaleLinear()
                .domain(d3.extent(this.data, d => d.value))
                .range([this.height - this.padding, 0 + this.padding]);

            this.svg.append("path")
                .datum(this.data.filter(d => !isNaN(d.value)))
                .attr("id", "sparkline-path")
                .attr("d", d3.line()
                    .curve(d3.curveCatmullRom.alpha(0.1))
                    .x(function(d) { return xScale(d.year) })
                    .y(function(d) { return yScale(d.value) })
                )
        }
    }
}
</script>

<style>
#sparkline-path {
    stroke: grey;
    stroke-width: 2px;
    fill: none;
}
</style>