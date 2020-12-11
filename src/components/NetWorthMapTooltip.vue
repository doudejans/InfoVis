<template>
    <div id="tooltip" class="absolute p-2 bg-white rounded border border-gray-200 border-solid shadow-md text-sm flex flex-col justify-between" :style="{left: mouseX + 20 + 'px', top: mouseY + 'px'}">
        <p class="font-bold font-serif">
                {{ regionName }}
        </p>
        <div class="flex h-16">
            <div class="mr-2 mt-2 flex flex-col w-32 h-full justify-center">
                <p class="font-light">
                    <span class="mr-2 text-xs font-bold text-gray-600 uppercase">{{valueDescription}}</span>
                    <div v-if="!isNaN(value)">
                        <span class="">{{value}}</span>
                        <span class="ml-1 text-xs text-gray-400">{{valueUnit}}</span>
                    </div>
                    <div class="" v-else>
                        No data available
                    </div>
                </p>
            </div>
            <div class="flex flex-col h-full w-32">
                <span class="text-xs text-gray-400 text-center w-full">8-year trend</span>
                <sparkline class="w-full h-full" :data="sparklineData"/>
            </div>
        </div>
        <hr class="mt-6 mb-2">
        <div class="w-64">
            <p class="">
                <span class="mr-2 text-xs font-bold text-gray-600 uppercase">{{featureGroup}}</span>
                <div class="font-light">{{householdFeature}}</div>
            </p>
            <div class="flex mt-2">
                <div class="flex-1">
                    <span class="mr-2 text-xs font-bold text-gray-600 uppercase">households</span>
                    <div class="font-light">
                        {{householdNumber}}
                        <span class="ml-1 text-xs text-gray-400">x 1000</span>
                    </div>
                </div>
                <div class="flex-1">
                    <span class="mr-2 text-xs font-bold text-gray-600 uppercase">of total</span>
                    <div class="font-light">{{householdPercentage}} %</div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Sparkline from './Sparkline.vue';

export default {
    components: { Sparkline },
    name: 'NetWorthMapTooltip',
    props: {
        regionName: String,
        mouseX: Number,
        mouseY: Number,
        valueDescription: String,
        value: Number,
        valueUnit: String,
        sparklineData: Array,
        featureGroup: String,
        householdFeature: String,
        householdNumber: Number,
        householdPercentage: Number,
    },
    data() {
        return {
        }
    },
    computed: {
    },
    methods: {
    }
}
</script>

<style scoped>
#tooltip {
    height: 250px;
}
</style>