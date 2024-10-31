<script setup lang="ts">
import { computed, defineModel } from "vue";

const model = defineModel();

const dateStart = computed(() => model.value.toLocaleDateString());
const dateEnd = computed(() => {
  let dateEndObject = new Date(model.value);
  dateEndObject.setDate(model.value.getDate() + 6);
  return dateEndObject.toLocaleDateString();
});

function incrementDate(delta: number) {
  let newDate = new Date(model.value);
  newDate.setDate(newDate.getDate() + delta);
  model.value = newDate;
}
</script>

<template>
  <div class="scroll-box">
    <button class="transparent eq" @click="incrementDate(-7)">
      <i class="bi bi-caret-left-fill"></i>
    </button>
    <span class="date-range">{{ dateStart }} &ndash; {{ dateEnd }}</span>
    <button class="transparent eq" @click="incrementDate(7)">
      <i class="bi bi-caret-right-fill"></i>
    </button>
  </div>
</template>

<style>
.scroll-box {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.date-range {
  font-weight: 700;
  width: 200px;
  text-align: center;
}
</style>
