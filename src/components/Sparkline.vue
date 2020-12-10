<template>
    <svg :width="width" :height="height" class="border"></svg>
</template>

<script>
export default {
    name: "Sparkline",
    props: {
        width: Number,
        height: Number,
    }
}
</script>