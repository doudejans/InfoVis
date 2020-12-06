<template>
    <div id="map">
        <svg width="960" height="960" viewbox="0 0 1000 1000"></svg>
        <net-worth-map-tooltip v-if="tooltipVisible" :regionName="activeRegionName" :mouseX="mouseX" :mouseY="mouseY" valueDescription="Mean wealth" :value="tooltipValue"/>
    </div>
</template>

<script>
import * as d3 from "d3";

import NetWorthMapTooltip from "./NetWorthMapTooltip.vue";

export default {
    name: 'NetWorthMap',
    props: {
        municipalityMap: Boolean
    },
    components: {
        NetWorthMapTooltip
    },
    data() {
        return {
            tooltipVisible: false,
            activeRegion: "",
            activeRegionName: "",
            tooltipValue: 0,
            mouseX: 0,
            mouseY: 0,
            data: []
        }
    },
    methods: {
        async initMap(municipalityMap) {
            console.log("hello")
            const svg = d3.select("#map").select("svg");
            const box = d3.select("#map").node();

            const width = box.getBoundingClientRect().width,
                height = box.getBoundingClientRect().height;
            svg.attr("width", width)
                .attr("height", height);

            var geoRegions;
            if (municipalityMap) {
                geoRegions = await d3.json("gemeente_2020.geojson");
            } else {
                geoRegions = await d3.json("provincie_2020.geojson");
            }

            const projection = d3.geoMercator().fitSize([width, height], geoRegions);
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
            const vm = this;

            var netWorth;
            if (municipalityMap) {
                netWorth = await d3.csv('vermogen_gemeenten_modified.csv');
            } else {
                netWorth = await d3.csv('vermogen_provincies_modified.csv');
            }
            this.data = netWorth.filter(n => n.Perioden == "2019JJ00").filter(n => n.KenmerkenHuishouden == "1050010");
            const extent = d3.extent(this.data, nw=> parseFloat(nw.GemiddeldVermogen_4));
            const colorScale = d3.scaleSequential(d3.interpolateViridis).domain(extent);

            svg.selectAll(".region")
                .attr("fill", function(d) {
                    const meanIncome = vm.data.find(nw => nw.RegioS == d.id).GemiddeldVermogen_4;
                    return meanIncome > 0 ? colorScale(parseFloat(meanIncome)) : 'lightgrey';
                })
                .on('mousemove', function(r) {
                    vm.showTooltip(r.srcElement.__data__, r.pageX, r.pageY);
                })
                .on('mouseout', function(r) {
                    vm.hideTooltip();
                });
        },
        redraw() {
            d3.select("#map").select("svg").selectAll("*").remove();
            this.initMap(this.municipalityMap);
            this.fillMap(this.municipalityMap);
        },
        showTooltip(data, mouseX, mouseY) {
            if (this.mouseX != mouseX || this.mouseY != mouseY || this.tooltipVisible == false) {
                if (this.activeRegion != data.id) {
                    this.activeRegion = data.id;
                    this.activeRegionName = data.properties.statnaam;
                    this.tooltipValue = parseFloat(this.data.find(nw => nw.RegioS == data.id).GemiddeldVermogen_4);
                }
                this.mouseX = mouseX;
                this.mouseY = mouseY;
                this.tooltipVisible = true;
            }
            
        },
        hideTooltip() {
            this.tooltipVisible = false;
            this.activeRegionName = "";
            this.activeRegion = "";
            this.mouseX = 0;
            this.mouseY = 0;
        }
    },
    async mounted() {
        this.initMap(this.municipalityMap);
        this.fillMap(this.municipalityMap);
        window.addEventListener('resize', this.redraw);
    },
    watch: {
        municipalityMap: function() {
            this.redraw()
        }
    }
}
</script>

<style>
path {
  stroke: #FFF;
  stroke-width: 0.2px;
}

</style>