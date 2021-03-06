<template>
    <div id="map">
        <svg width="960" height="960"></svg>
        <net-worth-map-tooltip
            v-if="tooltipVisible"
            :regionName="activeRegionName"
            :mouseX="mouseX"
            :mouseY="mouseY"
            :valueDescription="activeStatistic.capitalize() + ' wealth'"
            :value="tooltipValue"
            :valueUnit="activeStatistic == 'total' ? 'x 1B EUR' : 'x 1000 EUR'"
            :sparklineData="tooltipSparklineData" 
            :householdFeature="activeFeatureName"
            :featureGroup="activeFeatureGroup" 
            :householdNumber="tooltipHouseholdNumber"
            :householdPercentage="tooltipHouseholdPercentage"
            :tooltipHeight="tooltipHeight" 
            @changeHeight="setTooltipHeight"/>
    </div>
</template>

<script>
import * as d3 from "d3";
import {groupBy, range} from "lodash";
import { legendColor } from 'd3-svg-legend'

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
        activeFeatureName: String,
        activeFeatureGroup: String,
        activeYear: Number,
        wealthMunicipalities: Object,
        groupedFeaturesMunicipalities: Object,
        wealthProvinces: Object,
        groupedFeaturesProvinces: Object,
        municipalityRegions: Object,
        provinceRegions: Object,
        quantileScale: Boolean
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
            tooltipHouseholdNumber: 0,
            tooltipHouseholdPercentage: 0,
            tooltipHeight: 0,
            mouseX: 0,
            mouseY: 0,
            data: [],
            svg: null,
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
            const vm = this;

            const width = box.getBoundingClientRect().width,
                height = box.getBoundingClientRect().height;
            this.svg.attr("width", width)
                .attr("height", height)
                .on('click', function(r) {
                    vm.$emit('switchRegion', null);
                    vm.setStrokeRegion(null);
                });

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
        },
        fillMap(municipalityMap, activeStatistic, activeFeature, activeYear) {
            const vm = this;

            this.data = municipalityMap ? this.wealthMunicipalities : this.wealthProvinces;
            var features = municipalityMap ? this.groupedFeaturesMunicipalities : this.groupedFeaturesProvinces;

            const activeYearNetWorth = this.data[[activeYear + "JJ00", activeFeature]];
            const multiYearData = features[activeFeature].map(f => parseFloat(vm.getCurrentStatisticValue(f)));

            const domain = this.quantileScale ? multiYearData : d3.extent(multiYearData);

            const colorScale = d3.scaleQuantile().domain(domain)
                .range(d3.schemeGnBu[8]);

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
                })
                .on('click', function(r) {
                    vm.$emit('switchRegion', r.srcElement.__data__.id);
                    r.stopPropagation();
                    vm.setStrokeRegion(r.srcElement.__data__.id);
                });

            this.drawLegend(colorScale)
            this.tooltipHeight = 0;
            if (this.tooltipVisible) {
                const row = activeYearNetWorth.find(nw => nw.RegioS == this.activeRegion);
                this.tooltipValue = parseFloat(this.getCurrentStatisticValue(row));
                this.tooltipHouseholdNumber = +row.ParticuliereHuishoudens_1;
                this.tooltipHouseholdPercentage = +row.ParticuliereHuishoudensRelatief_2;
            }
        },
        drawLegend(colorScale) {
            const unit = this.activeStatistic == 'total' ? 'billions' : 'thousands'
            const legend = legendColor()
                .labelFormat(d3.format(".1f"))
                .title(this.activeStatistic.capitalize() + " wealth in " + unit)
                .scale(colorScale)
                .shapePadding(1)
                .shapeHeight(25);
            d3.select("#legend-wrapper").call(legend);
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
                    const row = this.data[[this.activeYear + "JJ00", this.activeFeature]].find(nw => nw.RegioS == data.id);
                    this.tooltipValue = parseFloat(this.getCurrentStatisticValue(row));
                    this.tooltipHouseholdNumber = +row.ParticuliereHuishoudens_1;
                    this.tooltipHouseholdPercentage = +row.ParticuliereHuishoudensRelatief_2;
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
        },
        setTooltipHeight(height) {
            this.tooltipHeight = height;
        },
        setStrokeRegion(regionId) {
            this.svg.selectAll(".region")
                .attr("stroke", "#333")
                .attr("stroke-width", 0.2);
            if (regionId) {
                this.svg.select("." + regionId)
                    .attr("stroke", "red")
                    .attr("stroke-width", 3)
                    .raise();
            }
        }
    },
    async mounted() {
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
            this.fillMap(this.municipalityMap, this.activeStatistic, this.activeFeature, this.activeYear);
        },
        quantileScale: function() {
            this.fillMap(this.municipalityMap, this.activeStatistic, this.activeFeature, this.activeYear);
        }
    }
}
</script>

<style>
#map {
  stroke: #333;
  stroke-width: 0.3px;
  cursor: pointer;
}

#legend-wrapper .label {
    @apply text-xs;
}

#legend-wrapper .swatch {
    stroke: none;
}

#legend-wrapper .legendTitle {
    @apply font-bold text-xs;
}
</style>
