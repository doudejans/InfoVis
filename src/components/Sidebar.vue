<template>
    <div>
        <div class="flex justify-center">
            <a class="button-group leftmost " :class="{ active: municipalityMap }" @click="toggleMunicipalityMap(true)">Municipalities</a>
            <a class="button-group rightmost " :class="{ active: !municipalityMap }" @click="toggleMunicipalityMap(false)">Provinces</a>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Sidebar',
    props: {
        municipalityMap: Boolean
    },
    data() {
        return {
        }
    },
    computed: {
    },
    methods: {
        toggleMunicipalityMap(value) {
            this.$emit('switchMap', value)
        }
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

.button-group.active {
  @apply bg-blue-800 text-white hover:bg-blue-700;
}
</style>
