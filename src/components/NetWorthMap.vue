<template>
    <div id="map">
        <svg width="960" height="960" viewbox="0 0 1000 1000"></svg>
        <net-worth-map-tooltip
            v-if="tooltipVisible"
            :regionName="activeRegionName"
            :mouseX="mouseX"
            :mouseY="mouseY"
            v-bind:valueDescription="this.activeStatistic.capitalize() + ' wealth'"
            :value="tooltipValue"
            v-bind:valueUnit="this.activeStatistic == 'total' ? 'mrd' : 'k'"/>
    </div>
</template>

<script>
import * as d3 from "d3";
import {groupBy} from "lodash";

import NetWorthMapTooltip from "./NetWorthMapTooltip.vue";

String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}

export default {
    name: 'NetWorthMap',
    props: {
        municipalityMap: Boolean,
        activeStatistic: String,
        activeFeature: String
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
            data: [],
            wealthMunicipalities: {},
            wealthProvinces: {},
            municipalityRegions: {},
            provinceRegions: {},
        }
    },
    methods: {
        getCurrentStatisticValue(row) {
            switch(this.activeStatistic) {
                case 'mean':
                    return row.GemiddeldVermogen_4;
                    break;
                case 'median':
                    return row.MediaanVermogen_5;
                    break;
                case 'total':
                    return row.TotaalVermogen_3;
                default:
                    return row.GemiddeldVermogen_4;
            }
        },
        initMap(municipalityMap) {
            const svg = d3.select("#map").select("svg");
            const box = d3.select("#map").node();

            const width = box.getBoundingClientRect().width,
                height = box.getBoundingClientRect().height;
            svg.attr("width", width)
                .attr("height", height);

            var geoRegions = municipalityMap ? this.municipalityRegions : this.provinceRegions;

            const projection = d3.geoMercator().fitSize([width, height], geoRegions);
            const path = d3.geoPath().projection(projection);

            svg.selectAll(".region")
                .data(geoRegions.features)
                .enter().append("path")
                .attr("class", function(d) { return "region " + d.id; })
                .attr("d", path)
                .attr("fill", "white");
        },
        fillMap(municipalityMap, activeStatistic, activeFeature) {
            const svg = d3.select("#map").select("svg");
            const vm = this;

            var netWorth = municipalityMap ? this.wealthMunicipalities : this.wealthProvinces;

            this.data = netWorth[["2019JJ00", activeFeature]];
            const extent = d3.extent(this.data, nw=> parseFloat(vm.getCurrentStatisticValue(nw)));
            const colorScale = d3.scaleSequential(d3.interpolateViridis).domain(extent);

            const map = new Map(this.data.map(row => [row.RegioS, row]))

            svg.selectAll(".region")
                .attr("fill", function(d) {
                    const meanIncome = vm.getCurrentStatisticValue(map.get(d.id));
                    return meanIncome != "." ? colorScale(parseFloat(meanIncome)) : 'lightgrey';
                })
                .on('mousemove', function(r) {
                    vm.showTooltip(r.srcElement.__data__, r.pageX, r.pageY);
                })
                .on('mouseout', function(r) {
                    vm.hideTooltip();
                });
        },
        filter() {
            
        },
        redraw() {
            d3.select("#map").select("svg").selectAll("*").remove();
            this.initMap(this.municipalityMap);
            this.fillMap(this.municipalityMap, this.activeStatistic, this.activeFeature);
        },
        showTooltip(data, mouseX, mouseY) {
            if (this.mouseX != mouseX || this.mouseY != mouseY || this.tooltipVisible == false) {
                if (this.activeRegion != data.id) {
                    this.activeRegion = data.id;
                    this.activeRegionName = data.properties.statnaam;
                    this.tooltipValue = parseFloat(this.getCurrentStatisticValue(this.data.find(nw => nw.RegioS == data.id)));
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
        const municipalityTable = await d3.csv('vermogen_gemeenten_modified.csv');
        this.wealthMunicipalities = groupBy(municipalityTable, w => [w.Perioden, w.KenmerkenHuishouden]);

        const provinceTable = await d3.csv('vermogen_provincies_modified.csv');
        this.wealthProvinces = groupBy(provinceTable, w => [w.Perioden, w.KenmerkenHuishouden]);

        this.municipalityRegions = await d3.json("gemeente_2020.geojson");
        this.provinceRegions = await d3.json("provincie_2020.geojson");

        this.initMap(this.municipalityMap);
        this.fillMap(this.municipalityMap, this.activeStatistic, this.activeFeature);
        window.addEventListener('resize', this.redraw);
    },
    watch: {
        municipalityMap: function() {
            this.redraw()
        },
        activeStatistic: function() {
            this.fillMap(this.municipalityMap, this.activeStatistic, this.activeFeature);
        },
        activeFeature: function() {
            this.fillMap(this.municipalityMap, this.activeStatistic, this.activeFeature);
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