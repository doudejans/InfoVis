<template>
    <div>
        <div class="flex justify-center">
            <a class="button-group leftmost " :class="{ active: municipalityMap }" @click="toggleMunicipalityMap(true)">Municipalities</a>
            <a class="button-group rightmost " :class="{ active: !municipalityMap }" @click="toggleMunicipalityMap(false)">Provinces</a>
        </div>

        <div class="flex justify-center my-2">
            <a class="button-group leftmost" :class="{ active: activeStatistic == 'mean' }" @click="setActiveStatistic('mean')">Mean</a>
            <a class="button-group" :class="{ active: activeStatistic == 'median' }" @click="setActiveStatistic('median')">Median</a>
            <a class="button-group rightmost" :class="{ active: activeStatistic == 'total' }" @click="setActiveStatistic('total')">Total</a>
        </div>

        <div class="flex-1 my-2">
            <ul>
                <li v-for="(value, name) in features" :key="name">
                    <a class="flex p-1 text-sm font-semibold text-gray-600 hover:bg-gray-50 rounded-md cursor-pointer select-none duration-200 ease-in-out"
                        @click="this.opened[name] = !this.opened[name]"
                    >
                        {{name}}
                    </a>
                    <ul v-if="this.opened[name]">
                        <li v-for="row in value" :key="row.Key">
                            <a class="flex ml-4 p-1 text-sm font-medium text-gray-500 hover:bg-gray-50 rounded-md cursor-pointer select-none duration-200 ease-in-out"
                                :class="{active: activeFeature == row.Key}"
                                @click="toggleActiveFeature(row.Key)">
                                {{row.Title}}
                            </a>
                        </li>
                    </ul>
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
import * as d3 from "d3";

export default {
    name: 'Sidebar',
    props: {
        municipalityMap: Boolean,
        activeStatistic: String,
        activeFeature: String
    },
    data() {
        return {
            features: {},
            opened: {}
        }
    },
    computed: {
    },
    methods: {
        toggleMunicipalityMap(value) {
            this.$emit('switchMap', value);
        },
        setActiveStatistic(value) {
            this.$emit('switchStatistic', value);
        },
        toggleActiveFeature(value) {
            this.$emit('switchFeature', value);
        }
    },
    async mounted() {
        const parsed_csv = await d3.csv("metadata_kenmerken_en.csv");

        var groupBy = function(xs, key) {
            return xs.reduce(function(rv, x) {
                (rv[x[key]] = rv[x[key]] || []).push(x);
                return rv;
            }, {});
        };

        this.features = groupBy(parsed_csv, 'Category');
        Object.keys(this.features).forEach(key => {
            this.opened[key] = false;
        });
    }
}
</script>

<style>
.button-group {
  @apply flex-1 inline-flex justify-center items-center px-2 border border-blue-800 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 cursor-pointer select-none duration-200 ease-in-out;
}

.button-group.leftmost {
  @apply rounded-l-md;
}

.button-group.rightmost {
  @apply rounded-r-md;
}

.active {
  @apply bg-blue-800 text-white hover:bg-blue-700;
}
</style>
