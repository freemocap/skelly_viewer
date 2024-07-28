<!-- src/components/FolderPicker.vue -->
<template>
  <div>
    <button @click="selectFolder">Select Folder</button>
    <p v-if="selectedPath">Selected Path: {{ selectedPath }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { dialog } from '@tauri-apps/api';

const selectedPath = ref('');

const selectFolder = async () => {
  try {
    const selected = await dialog.open({ directory: true });
    if (selected) {
      selectedPath.value = selected;
    }
  } catch (error) {
    console.error('Failed to select folder:', error);
  }
};
</script>

<style scoped>
button {
  margin-bottom: 1em;
}
</style>
