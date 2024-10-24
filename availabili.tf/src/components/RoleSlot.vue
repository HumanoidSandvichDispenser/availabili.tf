<script setup lang="ts">
const props = defineProps<{
  title: String,
}>();
</script>

<template>
  <div class="slot">
    <h1>{{ title }}</h1>
  </div>
</template>

<style scoped>
.slot {
  background-color: transparent;
  border: 2px solid var(--overlay-0);
  padding: 1em;
  border-radius: 8px;
}

h1 {
  font-size: 24px;
  color: var(--overlay-0);
}
</style>
