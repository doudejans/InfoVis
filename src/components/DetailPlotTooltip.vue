<template>
    <div 
    class="absolute p-2 bg-white rounded border border-gray-200 border-solid shadow-md text-sm"
    :style="{left: mouseX + 20 + 'px', top: mouseY + 'px'}">
        <span class="">{{value}}</span>
        <span class="ml-1 text-xs text-gray-400">{{valueUnit}}</span>
    </div>
</template>

<script>
export default {
    name: "DetailPlotTooltip",
    props: {
        value: String,
        valueUnit: String,
        mouseX: Number,
        mouseY: Number
    }
}
</script>