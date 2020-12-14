<template>
    <div id="plot">
        <detail-plot-tooltip
            v-if="tooltipVisible"
            :value="tooltipValue"
            :valueUnit="activeStatistic == 'total' ? 'x 1B EUR' : 'x 1000 EUR'" 
            :mouseX="mouseX"
            :mouseY="mouseY"/>
    </div>
</template>

<script>
import * as d3 from "d3";
import {groupBy} from "lodash";

import DetailPlotTooltip from "./DetailPlotTooltip.vue";

export default {
    name: 'DetailPlot',
    components: {
        DetailPlotTooltip
    },
    props: {
        activeStatistic: String,
        activeFeature: String,
        activeYear: Number,
        activeRegion: String,
        wealthMunicipalities: Object,
        groupedFeaturesMunicipalities: Object,
        wealthProvinces: Object,
        groupedFeaturesProvinces: Object,
        municipalityRegions: Object,
        provinceRegions: Object
    },
    data() {
        return {
            wealthNetherlands: null,
            svg: null,
            width: null,
            height: null,
            margin: {top: 5, right: 10, bottom: 30, left: 38},
            tooltipVisible: false,
            tooltipValue: 0,
            mouseX: 0,
            mouseY: 0
        }
    },
    computed: {
    },
    methods: {
        getCurrentStatisticValue(row) {
            switch(this.activeStatistic) {
                case 'mean':
                    return row.GemiddeldVermogen_4;
                case 'median':
                    return row.MediaanVermogen_5;
                case 'total':
                    return row.TotaalVermogen_3;
                default:
                    return row.GemiddeldVermogen_4;
            }
        },
        initPlot() {
            const box = d3.select("#plot").node();

            this.width = box.getBoundingClientRect().width;
            this.height = box.getBoundingClientRect().height;

            this.svg = d3.select("#plot")
                .append("svg")
                .attr("width", this.width)
                .attr("height", this.height);

            this.drawData();
        },
        drawData() {
            d3.select("#plot").select("svg").selectAll("*").remove();
            const vm = this;
            
            // Prepare the national data and optionally prepare the regional data
            var data = this.wealthNetherlands[[this.activeFeature]];
            var regionalData = [];
            if (this.activeRegion && this.activeRegion.includes("GM")) {
                regionalData = this.groupedFeaturesMunicipalities[[this.activeFeature]];
                regionalData = regionalData.filter(r => r.RegioS == this.activeRegion);
            } else if (this.activeRegion && this.activeRegion.includes("PV")) {
                regionalData = this.groupedFeaturesProvinces[[this.activeFeature]];
                regionalData = regionalData.filter(r => r.RegioS == this.activeRegion);
            }

            // Set the scales of the axes
            var x = d3.scaleTime()
                .domain([new Date(2010, 12), new Date(2019, 1)])
                .range([this.margin.left, this.width - this.margin.right]);
            
            var min = Math.min(0, d3.min(data, f => +vm.getCurrentStatisticValue(f)));
            var max = Math.max(0, d3.max(data, f => +vm.getCurrentStatisticValue(f)));
            if (regionalData.length > 0) {
                var minRegional = d3.min(regionalData, f => +vm.getCurrentStatisticValue(f));
                var maxRegional = d3.max(regionalData, f => +vm.getCurrentStatisticValue(f));
                if (!isNaN(minRegional) && !isNaN(maxRegional)) {
                    min = Math.min(min, minRegional);
                    max = Math.max(max, maxRegional);
                }
            }

            var y = d3.scaleLinear()
                .domain([min, max]).nice()
                .range([this.height - this.margin.bottom, this.margin.top]);

            // Draw the axes
            this.svg.append("g")
                .attr("transform", `translate(0,${this.height - this.margin.bottom})`)
                .call(d3.axisBottom(x))
                .select(".domain").remove();
            this.svg.append("g")
                .attr("transform", `translate(${this.margin.left},0)`)
                .call(d3.axisLeft(y)
                    .tickSizeOuter(0)
                    .tickSizeInner(10))
                .select(".domain").remove();
            
            // Draw the grid
            this.svg.selectAll("line.horizontalGrid").data(y.ticks()).enter()
                .append("line")
                    .attr("class", "grid")
                    .attr("x1", this.margin.left)
                    .attr("x2", this.width - this.margin.right)
                    .attr("y1", function(d){ return y(d);})
                    .attr("y2", function(d){ return y(d);})

            this.svg.selectAll("line.horizontalGrid").data(y.ticks()).enter()
                .append("line")
                    .attr("class", "grid-emph")
                    .attr("x1", this.margin.left)
                    .attr("x2", this.width - this.margin.right)
                    .attr("y1", y(0))
                    .attr("y2", y(0));

            // Draw the line and dots for the national data
            this.svg.append("path")
                .datum(data)
                .attr("class", "nl-line")
                .attr("d", d3.line()
                    .x(function(d) { return x(new Date(d.Perioden.slice(0, -4))) })
                    .y(function(d) { return y(vm.getCurrentStatisticValue(d)) })
                    );
            
            this.svg.selectAll("dots")
                .data(data)
                .enter()
                .append("circle")
                    .attr("class", "nl-line-dots")
                    .attr("cx", function(d) { return x(new Date(d.Perioden.slice(0, -4))) })
                    .attr("cy", function(d) { return y(vm.getCurrentStatisticValue(d)) })
                    .attr("r", 4)
                    .on("mouseover", e => {
                        this.tooltipVisible = true;
                        this.tooltipValue = vm.getCurrentStatisticValue(e.srcElement.__data__);
                        this.mouseX = e.pageX;
                        this.mouseY = e.pageY;
                    })
                    .on("mouseout", e => {
                        this.tooltipVisible = false;
                    });

            // Optionally draw the line and dots for the regional data
            if (regionalData.length > 0) {
                var line = d3.line()
                    .defined(d => !isNaN(vm.getCurrentStatisticValue(d)))
                    .x(function(d) { return x(new Date(d.Perioden.slice(0, -4))) })
                    .y(function(d) { return y(vm.getCurrentStatisticValue(d)) });

                this.svg.append("path")
                    .datum(regionalData.filter(line.defined()))
                    .attr("class", "alt-line")
                    .attr("stroke-dasharray", "4px")
                    .attr("d", line);
                
                this.svg.append("path")
                    .datum(regionalData)
                    .attr("class", "alt-line")
                    .attr("d", line);
                
                this.svg.selectAll("dots")
                    .data(regionalData.filter(d => !isNaN(vm.getCurrentStatisticValue(d))))
                    .enter()
                    .append("circle")
                        .attr("class", "alt-line-dots")
                        .attr("cx", function(d) { return x(new Date(d.Perioden.slice(0, -4))) })
                        .attr("cy", function(d) { return y(vm.getCurrentStatisticValue(d)) })
                        .attr("r", 4)
                        .on("mouseover", e => {
                            this.tooltipVisible = true;
                            this.tooltipValue = vm.getCurrentStatisticValue(e.srcElement.__data__);
                            this.mouseX = e.pageX;
                            this.mouseY = e.pageY;
                        })
                        .on("mouseout", e => {
                            this.tooltipVisible = false;
                        });
            }
            
            this.fillActiveYear();
        },
        fillActiveYear() {
            const vm = this;
            this.svg.selectAll("circle")
                .attr("class", function(d) {
                    var classes = d.RegioType == "Country" ? "nl-line-dots" : "alt-line-dots";
                    if (d.Perioden == vm.activeYear + "JJ00") {
                        classes += " active-dots";
                    }
                    return classes;
                });
        },
        redraw() {
            d3.select("#plot").selectAll("*").remove();
            this.initPlot();
        }
    },
    async mounted() {
        const netherlandsTable = await d3.csv('vermogen_nederland_modified.csv');
        this.wealthNetherlands = groupBy(netherlandsTable, w => [w.KenmerkenHuishouden]);

        this.redraw();
        window.addEventListener('resize', this.redraw);
    },
    watch: {
        activeStatistic: function() {
            this.drawData();
        },
        activeFeature: function() {
            this.drawData();
        },
        activeYear: function() {
            this.fillActiveYear();
        },
        activeRegion: function() {
            this.drawData();
        }
    }
}
</script>

<style>
#plot {
    @apply text-sm text-gray-500;
}

.active-dots {
    fill: white !important;
}

.nl-line {
    fill: none;
    stroke-width: 3;
    @apply stroke-current text-blue-800;
}

.nl-line-dots {
    @apply fill-current stroke-current text-blue-800;
}

.alt-line {
    fill: none;
    stroke-width: 3;
    @apply stroke-current text-red-800;
}

.alt-line-dots {
    @apply fill-current stroke-current text-red-800;
}

.grid {
    fill: none;
    shape-rendering: crispEdges;
    stroke-dasharray: 2px;

    @apply stroke-1 stroke-current text-gray-300;
}

.grid-emph {
    fill: none;
    shape-rendering: crispEdges;

    @apply stroke-1 stroke-current text-gray-400;
}

.tick line {
    visibility: hidden;
}
</style>
