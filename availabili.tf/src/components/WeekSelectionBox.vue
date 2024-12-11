<script setup lang="ts">
import { type Moment } from "moment";
import { computed, defineModel } from "vue";

const model = defineModel<Moment>({ required: true });

defineProps({
  isDisabled: Boolean,
});

const dateStart = computed(() => model.value.format("L"));
const dateEnd = computed(() => model.value.clone().add(6, "days").format("L"));

function incrementDate(delta: number) {
  model.value = model.value.clone().add(delta, "weeks");
  //let newDate = new Date(model.value);
  //newDate.setDate(newDate.getDate() + delta);
  //model.value = newDate;
}
</script>

<template>
  <div class="scroll-box">
    <button class="transparent eq" @click="incrementDate(-1)" :disabled="isDisabled">
      <i class="bi bi-caret-left-fill"></i>
    </button>
    <span class="date-range">{{ dateStart }} &ndash; {{ dateEnd }}</span>
    <button class="transparent eq" @click="incrementDate(1)" :disabled="isDisabled">
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
