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

            var data = this.wealthNetherlands[[this.activeFeature]];
            const vm = this;

            var x = d3.scaleTime()
                .domain([new Date(2010, 12), new Date(2019, 1)])
                .range([this.margin.left, this.width - this.margin.right]);

            const min = d3.min(data, f => +vm.getCurrentStatisticValue(f));
            const max = d3.max(data, f => +vm.getCurrentStatisticValue(f));

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
                    .attr("y2", function(d){ return y(d);});

            this.svg.append("path")
                .datum(data)
                .attr("class", "plotline")
                .attr("d", d3.line()
                    .curve(d3.curveCatmullRom.alpha(0.1))
                    .x(function(d) { return x(new Date(d.Perioden.slice(0, -4))) })
                    .y(function(d) { return y(vm.getCurrentStatisticValue(d)) })
                    );
            
            this.svg.selectAll("dots")
                .data(data)
                .enter()
                .append("circle")
                    .attr("stroke", "#1E40AF")
                    .attr("fill", "white")
                    .attr("cx", function(d) { return x(new Date(d.Perioden.slice(0, -4))) })
                    .attr("cy", function(d) { return y(vm.getCurrentStatisticValue(d)) })
                    .attr("r", 4)
            
            this.fillActiveYear();
        },
        fillActiveYear() {
            const vm = this;
            this.svg.selectAll("circle")
                .attr("fill", function(d) {
                    return d.Perioden == vm.activeYear + "JJ00" ? "white" : "#1E40AF";
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
        }
    }
}
</script>

<style>
#plot {
    @apply text-sm text-gray-500;
}

.plotline {
    fill: none;
    stroke: #1E40AF;
    stroke-width: 3;
}

.grid {
    fill: none;
    shape-rendering: crispEdges;
    stroke-dasharray: 2px;

    @apply stroke-1 stroke-current text-gray-300;
}

.tick line {
    visibility: hidden;
}
</style>
