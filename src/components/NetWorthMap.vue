<template>
    <div id="map">
        <svg width="960" height="960" viewbox="0 0 1000 1000"></svg>
        <net-worth-map-tooltip
            v-if="tooltipVisible"
            :regionName="activeRegionName"
            :mouseX="mouseX"
            :mouseY="mouseY"
            :valueDescription="activeStatistic.capitalize() + ' wealth'"
            :value="tooltipValue"
            :valueUnit="activeStatistic == 'total' ? 'b' : 'k'"/
            :sparklineData="tooltipSparklineData">
    </div>
</template>

<script>
import * as d3 from "d3";
import {groupBy, range} from "lodash";

import NetWorthMapTooltip from "./NetWorthMapTooltip.vue";

String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}

export default {
    name: 'NetWorthMap',
    props: {
        municipalityMap: Boolean,
        activeStatistic: String,
        activeFeature: String,
        activeYear: Number
    },
    components: {
        NetWorthMapTooltip
    },
    data() {
        return {
            tooltipVisible: false,
            activeRegion: "",
            activeRegionName: "",
            tooltipSparklineData: [],
            tooltipValue: 0,
            mouseX: 0,
            mouseY: 0,
            data: [],
            wealthMunicipalities: {},
            wealthProvinces: {},
            municipalityRegions: {},
            provinceRegions: {},
            svg: null
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
                    break;
                default:
                    return row.GemiddeldVermogen_4;
            }
        },
        initMap(municipalityMap) {
            this.svg = d3.select("#map").select("svg");
            const box = d3.select("#map").node();

            const width = box.getBoundingClientRect().width,
                height = box.getBoundingClientRect().height;
            this.svg.attr("width", width)
                .attr("height", height);

            var geoRegions = municipalityMap ? this.municipalityRegions : this.provinceRegions;

            const projection = d3.geoMercator().fitSize([width, height], geoRegions);
            const path = d3.geoPath().projection(projection);

            this.svg.selectAll(".region")
                .data(geoRegions.features)
                .enter().append("path")
                .attr("class", function(d) { return "region " + d.id; })
                .attr("d", path)
                .attr("fill", "white");

            this.svg.append("defs")
                .append("linearGradient")
                .attr("id", "linear-gradient")
                .attr("x1", "0%")
                .attr("y1", "0%")
                .attr("x2", "0%")
                .attr("y2", "100%")

            this.initLegend();
        },
        initLegend() {
            const legendWrapper = this.svg.append("g")
                .attr("id", "legend-wrapper")
                .attr("transform", "translate(0,20)");

            legendWrapper.append("rect")
                .attr("id", "legend-rect")
                .attr("y", 15);

            legendWrapper.append("text")
                .attr("id", "legend-title")
                .attr("y", 0);

            legendWrapper.append("g")
                .attr("id", "legend-axis")
                .attr("transform", "translate(0,15)");
        },
        fillMap(municipalityMap, activeStatistic, activeFeature, activeYear) {
            const vm = this;

            this.data = municipalityMap ? this.wealthMunicipalities : this.wealthProvinces;
            var features = municipalityMap ? this.groupedFeaturesMunicipalities : this.groupedFeaturesProvinces;

            const activeYearNetWorth = this.data[[activeYear + "JJ00", activeFeature]];

            const extent = d3.extent(features[activeFeature], f => parseFloat(vm.getCurrentStatisticValue(f)));
            const colorScale = d3.scaleSequential(d3.interpolateViridis).domain(extent);

            const map = new Map(activeYearNetWorth.map(row => [row.RegioS, row]))

            this.svg.selectAll(".region")
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

            this.drawLegend(colorScale)

            if (this.tooltipVisible) {
                this.tooltipValue = parseFloat(this.getCurrentStatisticValue(activeYearNetWorth.find(nw => nw.RegioS == this.activeRegion)));
            }
        },
        drawLegend(colorScale) {
            this.svg.select("#linear-gradient").selectAll("stop").remove();
            this.svg.select("#linear-gradient").selectAll("stop")
                .data(colorScale.ticks().reverse().map((t, i, n) => ({ offset: `${100*i/n.length}%`, color: colorScale(t) })))
                .enter().append("stop")
                .attr("offset", d => d.offset)
                .attr("stop-color", d => d.color);
            
            this.svg.select("#legend-rect")
                .attr("width", 12)
                .attr("height", 200)
                .style("fill", "url(#linear-gradient)");
            
            const axis = d3.axisRight(d3.scaleLinear().domain(colorScale.domain()).range([200, 0]))
                .ticks(5)
                .tickSize(12)
                .tickPadding(8);

            this.svg.select("#legend-axis")
                .call(axis);

            const unit = this.activeStatistic == 'total' ? 'billions' : 'thousands'

            this.svg.select("#legend-title")
                .text(this.activeStatistic.capitalize() + " wealth in " + unit);
        },
        redraw() {
            d3.select("#map").select("svg").selectAll("*").remove();
            this.initMap(this.municipalityMap);
            this.fillMap(this.municipalityMap, this.activeStatistic, this.activeFeature, this.activeYear);
        },
        showTooltip(data, mouseX, mouseY) {
            if (this.mouseX != mouseX || this.mouseY != mouseY || this.tooltipVisible == false) {
                if (this.activeRegion != data.id) {
                    this.activeRegion = data.id;
                    this.activeRegionName = data.properties.statnaam;
                    this.tooltipValue = parseFloat(this.getCurrentStatisticValue(this.data[[this.activeYear + "JJ00", this.activeFeature]].find(nw => nw.RegioS == data.id)));
                    this.tooltipSparklineData = range(2011, 2020).map(year => {return {
                        year: new Date("" + year),
                        value: parseFloat(this.getCurrentStatisticValue(this.data[[year + "JJ00", this.activeFeature]].find(nw => nw.RegioS == data.id)))
                    }});
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
        this.groupedFeaturesMunicipalities = groupBy(municipalityTable, w => [w.KenmerkenHuishouden]);

        const provinceTable = await d3.csv('vermogen_provincies_modified.csv');
        this.wealthProvinces = groupBy(provinceTable, w => [w.Perioden, w.KenmerkenHuishouden]);
        this.groupedFeaturesProvinces = groupBy(provinceTable, w => [w.KenmerkenHuishouden]);

        this.municipalityRegions = await d3.json("gemeente_2020.geojson");
        this.provinceRegions = await d3.json("provincie_2020.geojson");

        this.redraw();
        window.addEventListener('resize', this.redraw);
    },
    watch: {
        municipalityMap: function() {
            this.redraw()
        },
        activeStatistic: function() {
            this.fillMap(this.municipalityMap, this.activeStatistic, this.activeFeature, this.activeYear);
        },
        activeFeature: function() {
            this.fillMap(this.municipalityMap, this.activeStatistic, this.activeFeature, this.activeYear);
        },
        activeYear: function() {
            this.fillMap(this.municipalityMap, this.activeStatistic, this.activeFeature, this.activeYear)
        }
    }
}
</script>

<style>
path {
  stroke: #FFF;
  stroke-width: 0.2px;
}

#legend-title {
    @apply font-bold text-xs;
}

#legend-axis .tick line {
    color: white;
}

#legend-axis path {
    stroke: none;
}

#legend-axis .tick text {
   color: #333;
}


</style>