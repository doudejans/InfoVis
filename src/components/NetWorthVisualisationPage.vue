<template>
  <div class="container mx-auto p-4 h-screen flex flex-col">
    <h1 class="text-4xl font-serif">Household wealth distribution</h1>

    <div class="container mx-auto flex-1 flex">
      <net-worth-map class="flex w-2/3 m-2 max-h-screen"
        v-bind:municipalityMap="municipalityMap"
        v-bind:activeStatistic="activeStatistic"
        v-bind:activeFeature="activeFeature"
        v-bind:activeYear="activeYear"/>
      <sidebar class="w-1/3 m-2"
        v-bind:municipalityMap="municipalityMap"
        v-bind:activeStatistic="activeStatistic"
        v-bind:activeFeature="activeFeature"
        v-bind:activeYear="activeYear"
        @switchMap="switchMap"
        @switchStatistic="switchStatistic"
        @switchFeature="switchFeature"
        @switchYear="switchYear"/>
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
      municipalityMap: true,
      activeStatistic: 'mean',
      activeFeature: 1050010,
      activeYear: 2019
    }
  },
  methods: {
    switchMap(newValue) {
      this.municipalityMap = newValue;
    },
    switchStatistic(newValue) {
      this.activeStatistic = newValue;
    },
    switchFeature(newValue) {
      this.activeFeature = parseInt(newValue);
    },
    switchYear(newValue) {
      this.activeYear = parseInt(newValue);
    }
  }
}
</script>
