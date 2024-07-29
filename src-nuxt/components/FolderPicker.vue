<!-- src/components/FolderPicker.vue -->
<template>
  <div>
    <button @click="selectFolder">Select Folder</button>
    <p v-if="selectedPath">Selected Path: {{ recordingDataStore.recordingPath }}</p>
  </div>
</template>

<script setup>

import {dialog} from "@tauri-apps/api";

const recordingDataStore = useRecordingDataStore();


const selectFolder = async () => {
  try {
    const selected = await dialog.open({ directory: true });
    if (selected) {
      recordingDataStore.setRecordingPath(selected)
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
