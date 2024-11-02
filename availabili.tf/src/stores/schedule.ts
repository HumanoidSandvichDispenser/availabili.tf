import { computed } from "@vue/reactivity";
import { defineStore } from "pinia";
import { reactive, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

export const useScheduleStore = defineStore("schedule", () => {
  const dateStart = ref(new Date(2024, 9, 21, 0, 30));

  const windowStart = computed(() => Math.floor(dateStart.value.getTime() / 1000));

  const availability = reactive(new Array(168));

  const route = useRoute();
  const router = useRouter();

  const teamId = computed({
    get: () => route.query.teamId,
    set: (value) => router.push({ query: { teamId: value } }),
  });

  watch(dateStart, () => {
    availability.fill(0);
    fetchSchedule();
  });

  async function fetchSchedule() {
    return fetch(import.meta.env.VITE_API_BASE_URL + "/schedule?" + new URLSearchParams({
      window_start: windowStart.value.toString(),
      team_id: "1",
    }).toString(),{
        credentials: "include",
      })
      .then((response) => response.json())
      .then((response) => {
        response.availability.forEach((value: number, i: number) => {
          availability[i] = value;
        });
        return response;
      });
  }

  async function saveSchedule() {
    return fetch(import.meta.env.VITE_API_BASE_URL + "/schedule", {
      method: "PUT",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        window_start: Math.floor(dateStart.value.getTime() / 1000),
        team_id: 1,
        availability: availability,
      })
    });
  }

  return {
    dateStart,
    windowStart,
    availability,
    fetchSchedule,
    saveSchedule,
  };
});
