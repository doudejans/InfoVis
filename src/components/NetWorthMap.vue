<template>
    <div id="map"/>
</template>

<script>
import * as d3 from "d3";

export default {
    name: 'NetWorthMap',
    props: {
    },
    data() {
        return {
        }
    },
    mounted() {
        console.log('hallo');
        const width = 960,
            height = 1160;

        const svg = d3.select("body").append("svg")
            .attr("width", width)
            .attr("height", height);

        d3.json("gemeente_2020.geojson").then((regions) => {
             const projection = d3.geoMercator()
                 .scale(10000)
                 .center([0, 52])
                 .rotate([-4.8, 0])
                 .translate([width/2, height/2]);

            const path = d3.geoPath().projection(projection);

            svg.selectAll(".subunit")
                .data(regions.features)
                .enter().append("path")
                .attr("class", function(d) { return "region " + d.id; })
                .attr("d", path);
        });
    }

}
</script>

<style>
path {
  fill: none;
  stroke: #000;
  stroke-width: 0.5px;
}

.region.GM0383 {
    fill: lightgrey;
}

</style>