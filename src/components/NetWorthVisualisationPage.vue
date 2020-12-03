<template>
  <div class="container mx-auto p-4">
    <div class="flex-auto flex justify-between">
      <h1 class="text-4xl">Net worth</h1>
      <div class="flex">
        <a class="button-group leftmost" :class="{ active: municipalityMap }" @click="municipalityMap = true">Municipalities</a>
        <a class="button-group rightmost" :class="{ active: !municipalityMap }" @click="municipalityMap = false">Provinces</a>
      </div>
    </div>

    <net-worth-map v-bind:municipalityMap="municipalityMap"/>
  </div>
</template>

<script>
import NetWorthMap from "./NetWorthMap.vue";

export default {
  name: 'NetWorthVisualisationPage',
  components: {
    NetWorthMap
  },
  props: {
  },
  data() {
    return {
      municipalityMap: true
    }
  }
}
</script>

<style>
.button-group {
  @apply relative inline-flex items-center px-2 border border-blue-800 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 cursor-pointer select-none duration-200 ease-in-out;
}

.button-group.leftmost {
  @apply rounded-l-md;
}

.button-group.rightmost {
  @apply rounded-r-md;
}

.button-group.active {
  @apply bg-blue-800 text-white hover:bg-blue-700;
}
</style>
