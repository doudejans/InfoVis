<template>
    <div id="plot">
    </div>
</template>

<script>
import * as d3 from "d3";
import {groupBy} from "lodash";

export default {
    name: 'DetailPlot',
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
            margin: {top: 5, right: 10, bottom: 30, left: 38}
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
            
            var data = this.wealthNetherlands[[this.activeFeature]];
            var regionalData = [];
            if (this.activeRegion && this.activeRegion.includes("GM")) {
                regionalData = this.groupedFeaturesMunicipalities[[this.activeFeature]];
                regionalData = regionalData.filter(r => r.RegioS == this.activeRegion);
            } else if (this.activeRegion && this.activeRegion.includes("PV")) {
                regionalData = this.groupedFeaturesProvinces[[this.activeFeature]];
                regionalData = regionalData.filter(r => r.RegioS == this.activeRegion);
            }

            var x = d3.scaleTime()
                .domain([new Date(2010, 12), new Date(2019, 1)])
                .range([this.margin.left, this.width - this.margin.right]);

            var min = Math.min(0, d3.min(data, f => +vm.getCurrentStatisticValue(f)));
            var max = Math.max(0, d3.max(data, f => +vm.getCurrentStatisticValue(f)));
            if (regionalData.length > 0) {
                min = Math.min(min, d3.min(regionalData, f => +vm.getCurrentStatisticValue(f)));
                max = Math.max(max, d3.max(regionalData, f => +vm.getCurrentStatisticValue(f)));
            }

            var y = d3.scaleLinear()
                .domain([min, max])
                .range([this.height - this.margin.bottom, this.margin.top]);

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

            this.svg.append("path")
                .datum(data)
                .attr("class", "nl-line")
                .attr("d", d3.line()
                    .curve(d3.curveCatmullRom.alpha(0.1))
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

            if (regionalData.length > 0) {
                this.svg.append("path")
                .datum(regionalData)
                .attr("class", "alt-line")
                .attr("d", d3.line()
                    .curve(d3.curveCatmullRom.alpha(0.1))
                    .x(function(d) { return x(new Date(d.Perioden.slice(0, -4))) })
                    .y(function(d) { return y(vm.getCurrentStatisticValue(d)) })
                    );
            
            this.svg.selectAll("dots")
                .data(regionalData)
                .enter()
                .append("circle")
                    .attr("class", "alt-line-dots")
                    .attr("cx", function(d) { return x(new Date(d.Perioden.slice(0, -4))) })
                    .attr("cy", function(d) { return y(vm.getCurrentStatisticValue(d)) })
                    .attr("r", 4)
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
