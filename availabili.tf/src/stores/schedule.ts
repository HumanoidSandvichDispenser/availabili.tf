import { defineStore } from "pinia";
import { reactive, ref, watch } from "vue";

export const useScheduleStore = defineStore("schedule", () => {
  const dateStart = ref(new Date(2024, 9, 21));

  const availability = reactive(new Array(168));

  watch(dateStart, () => {
    availability.fill(0);
  });

  return {
    dateStart,
    availability,
  };
});
