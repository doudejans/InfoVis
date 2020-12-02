<template>
  <div class="container mx-auto p-4">
    <h1 class="text-4xl">Net worth per province</h1>
    <net-worth-map/>
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
    }
  }
}
</script>
