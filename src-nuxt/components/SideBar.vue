
<template>
  <v-navigation-drawer v-model="drawer" app :rail="rail" class="bg-cyan-darken-4">
    <v-list class="pa-0">
      <v-list-item :class="drawer ? 'justify-end' : 'justify-center'" class="px-3 d-flex" @click="toggleRail">
        <v-icon large class="clickable">
          {{ railIcon }}
        </v-icon>
      </v-list-item>
      <v-list-item :class="drawer ? 'justify-end' : 'justify-center'" class="px-3 d-flex">
        <NuxtLink to="/">
          🏠
        </NuxtLink>
      </v-list-item>
      <v-list-item :class="drawer ? 'justify-end' : 'justify-center'" class="px-3 d-flex">
        <NuxtLink to="/cameras">
          📸
        </NuxtLink>
      </v-list-item>
      <v-list-item :class="drawer ? 'justify-end' : 'justify-center'" class="px-3 d-flex">
        <FolderPicker />
      </v-list-item>

    </v-list>
  </v-navigation-drawer>
</template>
<script setup lang="ts">

const drawer = ref(true);
const rail = ref(true);

const railIcon = computed(() => (rail.value ? 'mdi-cog' : 'mdi-chevron-left'));

const toggleRail = () => {
  console.log('toggleRail');
  rail.value = !rail.value;

  if (rail.value) {
    drawer.value = true;
  }
}
</script>

<style scoped>
.clickable {
  cursor: pointer;
}
</style>
