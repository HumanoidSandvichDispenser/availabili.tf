import { computed } from "@vue/reactivity";
import { defineStore } from "pinia";
import { reactive, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useClientStore } from "./client";

export const useScheduleStore = defineStore("schedule", () => {
  const client = useClientStore().client;

  const dateStart = ref(new Date(2024, 9, 21, 0, 30));

  const windowStart = computed(() => Math.floor(dateStart.value.getTime() / 1000));

  const availability = reactive(new Array(168));

  availability.fill(0);

  const route = useRoute();
  const router = useRouter();

  const teamId = computed({
    get: () => Number(route.query.teamId),
    set: (value) => router.push({ query: { teamId: value } }),
  });

  watch(dateStart, () => {
    fetchSchedule();
  });

  watch(teamId, () => {
    fetchSchedule();
  });

  async function fetchSchedule() {
    return client.default.getApiSchedule(
      Math.floor(dateStart.value.getTime() / 1000).toString(),
      teamId.value,
    )
      .then((response) => {
        response.availability.forEach((value, i) => {
          availability[i] = value;
        });
        return response;
      });
    //return fetch(import.meta.env.VITE_API_BASE_URL + "/schedule?" + new URLSearchParams({
    //  window_start: windowStart.value.toString(),
    //  team_id: teamId.toString(),
    //}).toString(),{
    //    credentials: "include",
    //  })
    //  .then((response) => response.json())
    //  .then((response) => {
    //    response.availability.forEach((value: number, i: number) => {
    //      availability[i] = value;
    //    });
    //    return response;
    //  });
  }

  async function saveSchedule() {
    return client.default.putApiSchedule({
      windowStart: Math.floor(dateStart.value.getTime() / 1000).toString(),
      teamId: teamId.value,
      availability,
    });
    //return fetch(import.meta.env.VITE_API_BASE_URL + "/schedule", {
    //  method: "PUT",
    //  credentials: "include",
    //  headers: {
    //    "Content-Type": "application/json",
    //  },
    //  body: JSON.stringify({
    //    window_start: Math.floor(dateStart.value.getTime() / 1000),
    //    team_id: teamId.toString(),
    //    availability: availability,
    //  })
    //});
  }

  return {
    dateStart,
    windowStart,
    availability,
    fetchSchedule,
    saveSchedule,
    teamId,
  };
});
