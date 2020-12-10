<template>
  <div class="container mx-auto p-4 h-screen flex flex-col">
    <h1 class="text-4xl font-serif">Household wealth distribution</h1>

    <div class="container mx-auto flex-1 flex mt-2">
      <net-worth-map v-if="provinceRegions" class="flex w-2/3 mr-2 mb-2 max-h-screen"
        :municipalityMap="municipalityMap"
        :activeStatistic="activeStatistic"
        :activeFeature="activeFeature"
        :activeYear="activeYear"
        :wealthMunicipalities="wealthMunicipalities"
        :groupedFeaturesMunicipalities="groupedFeaturesMunicipalities"
        :wealthProvinces="wealthProvinces"
        :groupedFeaturesProvinces="groupedFeaturesProvinces"
        :municipalityRegions="municipalityRegions"
        :provinceRegions="provinceRegions"/>

      <div class="container w-1/3 ml-2 mb-2">
        <detail-plot v-if="provinceRegions" class="flex w-full"
          :activeFeature="activeFeature"
          :activeStatistic="activeStatistic"
          :activeYear="activeYear"
          :wealthMunicipalities="wealthMunicipalities"
          :groupedFeaturesMunicipalities="groupedFeaturesMunicipalities"
          :wealthProvinces="wealthProvinces"
          :groupedFeaturesProvinces="groupedFeaturesProvinces"
          :municipalityRegions="municipalityRegions"
          :provinceRegions="provinceRegions"/>

        <sidebar class="mt-2 w-full"
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
  </div>
</template>

<script>
import * as d3 from "d3";
import {groupBy} from "lodash";
import NetWorthMap from "./NetWorthMap.vue";
import Sidebar from "./Sidebar.vue";
import DetailPlot from "./DetailPlot.vue";

export default {
  name: 'NetWorthVisualisationPage',
  components: {
    NetWorthMap,
    Sidebar,
    DetailPlot
  },
  props: {
  },
  data() {
    return {
      municipalityMap: true,
      activeStatistic: 'mean',
      activeFeature: '1050010',
      activeYear: 2019,
      wealthMunicipalities: null,
      groupedFeaturesMunicipalities: null,
      wealthProvinces: null,
      groupedFeaturesProvinces: null,
      municipalityRegions: null,
      provinceRegions: null,
    }
  },
  async mounted() {
    const municipalityTable = await d3.csv('vermogen_gemeenten_modified.csv');
      this.wealthMunicipalities = groupBy(municipalityTable, w => [w.Perioden, w.KenmerkenHuishouden]);
      this.groupedFeaturesMunicipalities = groupBy(municipalityTable, w => [w.KenmerkenHuishouden]);

      const provinceTable = await d3.csv('vermogen_provincies_modified.csv');
      this.wealthProvinces = groupBy(provinceTable, w => [w.Perioden, w.KenmerkenHuishouden]);
      this.groupedFeaturesProvinces = groupBy(provinceTable, w => [w.KenmerkenHuishouden]);

      this.municipalityRegions = await d3.json("gemeente_2020.geojson");
      this.provinceRegions = await d3.json("provincie_2020.geojson");
  },
  methods: {
    switchMap(newValue) {
      this.municipalityMap = newValue;
    },
    switchStatistic(newValue) {
      this.activeStatistic = newValue;
    },
    switchFeature(newValue) {
      this.activeFeature = newValue.toString();
    },
    switchYear(newValue) {
      this.activeYear = parseInt(newValue);
    }
  }
}
</script>
