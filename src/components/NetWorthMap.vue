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
                .attr("d", path)
                .attr("fill", "white");
        },
        async fillMap(municipalityMap) {
            const svg = d3.select("#map").select("svg");

            var netWorth;
            if (municipalityMap) {
                netWorth = await d3.csv('vermogen_gemeenten_modified.csv');
            } else {
                netWorth = await d3.csv('vermogen_provincies_modified.csv');
            }
            const nw2019 = netWorth.filter(n => n.Perioden == "2019JJ00").filter(n => n.KenmerkenHuishouden == "1050010");
            const extent = d3.extent(nw2019, nw=> parseFloat(nw.GemiddeldVermogen_4));
            const colorScale = d3.scaleSequential(d3.interpolateBlues).domain(extent);

            svg.selectAll(".region")
                .attr("fill", function(d) { 
                    const meanIncome = nw2019.find(nw => nw.RegioS == d.id).GemiddeldVermogen_4;
                    return colorScale(parseFloat(meanIncome))
                });
        }
    },
    async mounted() {
        this.initMap(this.municipalityMap)
        this.fillMap(this.municipalityMap)
    },
    watch: {
        municipalityMap: function() {
            d3.select("#map").select("svg").remove();
            this.initMap(this.municipalityMap);
            this.fillMap(this.municipalityMap);
        }
    }
}
</script>

<style>
path {
  stroke: #000;
  stroke-width: 0.5px;
}

</style>