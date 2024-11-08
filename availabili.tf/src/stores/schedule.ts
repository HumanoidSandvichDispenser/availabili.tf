import { computed } from "@vue/reactivity";
import { defineStore } from "pinia";
import { reactive, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useClientStore } from "./client";
import type { TeamSchema } from "@/client";
import moment from "moment";
import "moment-timezone";

export const useScheduleStore = defineStore("schedule", () => {
  const client = useClientStore().client;

  const dateStart = ref(new Date(2024, 9, 21, 0, 30));

  const windowStart = computed(() => Math.floor(dateStart.value.getTime() / 1000));

  const availability = reactive(new Array(168));

  availability.fill(0);

  const route = useRoute();
  const router = useRouter();

  //const teamId = computed({
  //  get: () => Number(route?.query?.teamId),
  //  set: (value) => router.push({ query: { teamId: value } }),
  //});
  const team = ref();

  function getWindowStart(team: TeamSchema) {
    // convert local 00:00 to league timezone
    let localMidnight = moment().startOf("isoWeek");
    let leagueTime = localMidnight.clone().tz(team.tzTimezone);

    let nextMinuteOffsetTime = leagueTime.clone();

    if (nextMinuteOffsetTime.minute() > team.minuteOffset) {
      nextMinuteOffsetTime.add(1, "hour");
    }

    nextMinuteOffsetTime.minute(team.minuteOffset);

    const deltaMinutes = nextMinuteOffsetTime.diff(leagueTime, "minutes");

    return localMidnight.clone().add(deltaMinutes, "minutes");
  }

  watch(dateStart, () => {
    fetchSchedule();
  });

  watch(team, () => {
    dateStart.value = getWindowStart(team.value).toDate();
    console.log(dateStart.value);
  });

  async function fetchSchedule() {
    return client.default.getApiSchedule(
      Math.floor(dateStart.value.getTime() / 1000).toString(),
      team.value.id,
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
      teamId: team.value.id,
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
    team,
    getWindowStart,
  };
});
