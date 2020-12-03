<template>
    <div id="map"/>
</template>

<script>
import * as d3 from "d3";

export default {
    name: 'NetWorthMap',
    props: {
        municipalityMap: Boolean
    },
    data() {
        return {
        }
    },
    methods: {
        async initMap(municipalityMap) {
            const width = 960,
            height = 1160;

            const svg = d3.select("#map").append("svg")
                .attr("width", width)
                .attr("height", height);

            var geoRegions;
            if (municipalityMap) {
                geoRegions = await d3.json("gemeente_2020.geojson");
            } else {
                geoRegions = await d3.json("provincie_2020.geojson");
            }

            const projection = d3.geoMercator()
                .scale(10000)
                .center([0, 52])
                .rotate([-4.8, 0])
                .translate([width/2, height/2]);

            const path = d3.geoPath().projection(projection);

            svg.selectAll(".region")
                .data(geoRegions.features)
                .enter().append("path")
                .attr("class", function(d) { return "region " + d.id; })
                .attr("d", path);
        }
    },
    async mounted() {
        this.initMap(this.municipalityMap)
    },
    watch: {
        municipalityMap: function() {
            d3.select("svg").remove();
            this.initMap(this.municipalityMap);
        }
    }

}
</script>

<style>
path {
  fill: none;
  stroke: #000;
  stroke-width: 0.5px;
}

</style>