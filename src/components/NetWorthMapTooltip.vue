<template>
    <div id="tooltip" class="absolute p-2 bg-white rounded border border-gray-200 border-solid shadow-md text-sm flex" :style="{left: mouseX + 'px', top: mouseY + 20 + 'px'}">
        <div class="mr-2">
            <p class="font-bold font-serif">
                {{ regionName }}
            </p>
            <p class="font-light">
                <span class="mr-2">{{valueDescription}}:</span>
                <div v-if="!isNaN(value)">
                    <span class="">{{value}}</span>
                    <span>{{valueUnit}} EUR</span>
                </div>
                <div class="" v-else>
                    No data available
                </div>
            </p>
        </div>
        <div class="flex flex-col">
            <span class="text-xs text-gray-400 text-center">8-year trend</span>
            <sparkline class="w-32 h-14" :data="sparklineData"/>
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
        sparklineData: Array
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

