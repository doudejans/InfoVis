<template>
  <div class="container mx-auto p-4 h-screen flex flex-col">
    <h1 class="text-4xl font-serif">Household wealth distribution</h1>
    <div class="container mx-auto flex-1 flex">
      <net-worth-map v-if="provinceRegions" class="flex w-2/3 mr-2 mb-2 max-h-screen"
        :municipalityMap="municipalityMap"
        :activeStatistic="activeStatistic"
        :activeFeature="activeFeature"
        :activeFeatureName="activeFeatureName"
        :activeFeatureGroup="activeFeatureGroup"
        :activeYear="activeYear"
        :wealthMunicipalities="wealthMunicipalities"
        :groupedFeaturesMunicipalities="groupedFeaturesMunicipalities"
        :wealthProvinces="wealthProvinces"
        :groupedFeaturesProvinces="groupedFeaturesProvinces"
        :municipalityRegions="municipalityRegions"
        :provinceRegions="provinceRegions"
        @switchRegion="switchRegion"/>

      <div class="w-1/3 ml-2 mb-2">
        <h2 class="text-xl font-serif">{{activeStatistic.capitalize()}} wealth over time</h2>
        <div class="flex justify-between">
          <h3 class="text-xs uppercase font-bold text-gray-600 mb-2" v-if="!activeRegion">Netherlands</h3>
          <h3 class="text-xs uppercase font-bold text-gray-600 mb-2" v-if="activeRegion"><span class="text-blue-800">Netherlands</span> & <span class="text-red-800">{{getRegionName(activeRegion)}}</span></h3>
          <h4 class="text-xs font-light text-gray-400 text-right">{{activeStatistic == "total" ? "x 1B EUR" : "x 1000 EUR"}}</h4>
        </div>
        <detail-plot v-if="provinceRegions" class="flex w-full h-52"
          :activeFeature="activeFeature"
          :activeStatistic="activeStatistic"
          :activeYear="activeYear"
          :activeRegion="activeRegion"
          :wealthMunicipalities="wealthMunicipalities"
          :groupedFeaturesMunicipalities="groupedFeaturesMunicipalities"
          :wealthProvinces="wealthProvinces"
          :groupedFeaturesProvinces="groupedFeaturesProvinces"
          :municipalityRegions="municipalityRegions"
          :provinceRegions="provinceRegions"/>

        <sidebar class="mt-4 w-full"
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
      activeFeatureGroup: "Total",
      activeFeatureName: "Private households",
      activeYear: 2019,
      activeRegion: null,
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
    switchFeature({feature, featureName, featureGroup}) {
      this.activeFeature = feature.toString();
      this.activeFeatureName = featureName;
      this.activeFeatureGroup = featureGroup;
    },
    switchYear(newValue) {
      this.activeYear = parseInt(newValue);
    },
    switchRegion(regionId) {
      this.activeRegion = regionId;
    },
    getRegionName(regionId) {
      if (!regionId) {
        return "Netherlands";
      }

      if (regionId.includes("GM")) {
        return this.municipalityRegions.features.find(r => r.id == regionId).properties.statnaam;
      } else if (regionId.includes("PV")) {
        return this.provinceRegions.features.find(r => r.id == regionId).properties.statnaam;
      }
      return "Netherlands"
    }
  }
}
</script>
