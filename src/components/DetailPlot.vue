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
            height: null
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

            var margin = {top: 5, right: 40, bottom: 20, left: 40};

            this.width = box.getBoundingClientRect().width - margin.left - margin.right;
            this.height = box.getBoundingClientRect().height - margin.top - margin.bottom;

            this.svg = d3.select("#plot")
                .append("svg")
                    .attr("width", this.width + margin.left + margin.right)
                    .attr("height", this.height + margin.top + margin.bottom)
                .append("g")
                    .attr("transform",
                        "translate(" + margin.left + "," + margin.top + ")");

            this.drawData();
        },
        drawData() {
            d3.select("#plot").select("svg").select("g").selectAll("*").remove();
            var data = this.wealthNetherlands[[this.activeFeature]];

            var x = d3.scaleTime().domain([new Date('2010'), new Date('2019')]).range([0, this.width]);
            this.svg.append("g")
                .attr("transform", "translate(0," + this.height + ")")
                .call(d3.axisBottom(x));

            const vm = this;
            var y = d3.scaleLinear().domain([0, d3.max(data, f => +vm.getCurrentStatisticValue(f))]).range([this.height, 0]);
            this.svg.append("g")
                .call(d3.axisLeft(y));

            this.svg.append("path")
                .datum(data)
                .attr("class", "plotline")
                .attr("d", d3.line()
                    .curve(d3.curveCatmullRom.alpha(0.1))
                    .x(function(d) { return x(new Date(d.Perioden.slice(0, -4))) })
                    .y(function(d) { return y(vm.getCurrentStatisticValue(d)) })
                    );
        },
        redraw() {
            d3.select("#plot").selectAll("*").remove();
            this.initPlot();
        },
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
        }
    }
}
</script>

<style>
.plotline {
    fill: none;
    stroke: #1E40AF;
    stroke-width: 3;
}
</style>
