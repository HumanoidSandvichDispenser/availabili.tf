<script setup lang="ts">
import { ContentLoader } from "vue-content-loader";

const props = defineProps<{
  width?: string;
  height?: string;
  speed?: number;
}>();

// get primary color from var(--overlay-0) and secondary from var(--overlay-1)
const primaryColor = getComputedStyle(document.documentElement).getPropertyValue("--surface-0");

const secondaryColor = getComputedStyle(document.documentElement).getPropertyValue("--overlay-0");
</script>

<template>
  <!--ContentLoader :width="width" :height="height" :speed="speed">
  </ContentLoader-->
  <component :is="ContentLoader" v-bind="{ ...props, primaryColor, secondaryColor }">
    <slot></slot>
  </component>
</template>

<style scoped>
.loader-container {
  display: flex;
  width: 100%;
  justify-content: center;
  align-items: center;
}
</style>
