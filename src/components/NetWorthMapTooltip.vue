<template>
    <div id="tooltip" class="absolute p-3 bg-white rounded border border-gray-200 border-solid shadow-md" :style="{left: mouseX + 'px', top: mouseY + 20 + 'px'}">
        {{ regionName }}
    </div>
</template>

<script>
export default {
    name: 'NetWorthMapTooltip',
    props: {
        regionName: String,
        mouseX: Number,
        mouseY: Number,
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

