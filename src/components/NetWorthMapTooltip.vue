<template>
    <div id="tooltip" class="absolute p-2 bg-white rounded border border-gray-200 border-solid shadow-md text-sm flex items-center" :style="{left: mouseX + 'px', top: mouseY + 20 + 'px'}">
        <div class="mr-2">
            <p class="font-bold font-serif">
                {{ regionName }}
            </p>
            <p class="font-light">
                <span class="mr-2">{{valueDescription}}:</span>
                <div v-if="value">
                    <span class="">{{value}}</span>
                    <span>{{valueUnit}} EUR</span>
                </div>
                <div class="" v-else>
                    No data available
                </div>
            </p>
        </div>
        <sparkline width=100 height=50 />
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
        valueUnit: String
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

