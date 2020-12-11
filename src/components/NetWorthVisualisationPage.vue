<template>
  <div class="container mx-auto p-4 h-screen flex flex-col">
    <h1 class="text-4xl font-serif">Household wealth distribution</h1>

    <div class="container mx-auto flex-1 flex">
      <net-worth-map class="flex w-2/3 mt-2 mr-2 mb-2 max-h-screen"
        :municipalityMap="municipalityMap"
        :activeStatistic="activeStatistic"
        :activeFeature="activeFeature"
        :activeYear="activeYear"
        :activeFeatureName="activeFeatureName"
        :activeFeatureGroup="activeFeatureGroup" />
      <sidebar class="w-1/3 mt-2 ml-2 mb-2"
        :municipalityMap="municipalityMap"
        :activeStatistic="activeStatistic"
        :activeFeature="activeFeature"
        :activeYear="activeYear"
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
      activeFeature: '1050010',
      activeYear: 2019,
      activeFeatureGroup: "Total",
      activeFeatureName: "Private households"
    }
  },
  methods: {
    switchMap(newValue) {
      this.municipalityMap = newValue;
    },
    switchStatistic(newValue) {
      this.activeStatistic = newValue;
    },
    switchFeature({feature, featureName, featureGroup}) {
      this.activeFeature = feature.toString();
      this.activeFeatureName = featureName;
      this.activeFeatureGroup = featureGroup;
    },
    switchYear(newValue) {
      this.activeYear = parseInt(newValue);
    }
  }
}
</script>
