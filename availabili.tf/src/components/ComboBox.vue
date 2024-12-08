<script setup lang="ts" generic="T extends AcceptableValue">
import { defineModel, defineProps, ref } from "vue";
import {
  ComboboxContent,
  ComboboxInput,
  ComboboxItem,
  ComboboxRoot,
  ComboboxPortal,
  ComboboxTrigger,
  ComboboxAnchor,
  ComboboxViewport,
} from "radix-vue";
import type { AcceptableValue } from "node_modules/radix-vue/dist/shared/types";

const selectedValue = defineModel<T>();

const isOpen = ref(false);

withDefaults(defineProps<{
  values: T[];
  //mapper? (value: T): string;
  //keyMapper? (value: T): string;
  display: string;
  keyField: string;
}>(), {
  //mapper: (value: T) => value.toString(),
});
</script>

<template>
  <ComboboxRoot
    v-model="selectedValue"
    v-model:open="isOpen"
    defaultOpen
  >
    <ComboboxAnchor>
      <ComboboxInput />
      <ComboboxTrigger>
        hi
      </ComboboxTrigger>
    </ComboboxAnchor>

    <ComboboxPortal>
      <ComboboxContent position="popper">
        <ComboboxViewport>
        </ComboboxViewport>
      </ComboboxContent>
    </ComboboxPortal>
  </ComboboxRoot>
</template>

<style scoped>
</style>
