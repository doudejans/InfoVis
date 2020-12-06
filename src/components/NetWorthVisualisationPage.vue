<template>
  <div class="container mx-auto p-4 h-screen flex flex-col">
    <h1 class="text-4xl font-serif">Household wealth distribution</h1>

    <div class="container mx-auto flex-1 flex">
      <net-worth-map class="flex w-2/3 m-2" v-bind:municipalityMap="municipalityMap"/>
      <sidebar class="w-1/3 m-2" v-bind:municipalityMap="municipalityMap" @switchMap="switchMap"/>
    </div>
  </div>
</template>

<script>
import NetWorthMap from "./NetWorthMap.vue";
import Sidebar from "./Sidebar.vue";

export default {
  name: 'NetWorthVisualisationPage',
  components: {
    NetWorthMap,
    Sidebar
  },
  props: {
  },
  data() {
    return {
      municipalityMap: true
    }
  },
  methods: {
    switchMap(newValue) {
      this.municipalityMap = newValue;
    }
  }
}
</script>
