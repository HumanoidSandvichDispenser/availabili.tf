<script setup lang="ts">
</script>

<template>
  <div class="loader">
  </div>
</template>

<style scoped>
.loader {
  width: 12px;
  aspect-ratio: 1;
  border-radius: 50%;
  animation: loader-anim 1s infinite linear;
}

@keyframes loader-anim {
  0%  {
    box-shadow: 20px 4px var(--overlay-0), -20px -4px var(--overlay-0);
    background: var(--overlay-0);
  }
  25% {
    box-shadow: 20px 0 var(--overlay-0), -20px 0 var(--overlay-0);
    background: var(--overlay-0);
  }
  50% {
    box-shadow: 20px -4px var(--overlay-0), -20px 4px var(--overlay-0);
    background: var(--overlay-0);
  }
  75% {
    box-shadow: 20px 0 var(--overlay-0), -20px 0 var(--overlay-0);
    background: var(--overlay-0);
  }
  100% {
    box-shadow: 20px 4px var(--overlay-0), -20px -4px var(--overlay-0);
    background: var(--overlay-0);
  }
}
</style>
