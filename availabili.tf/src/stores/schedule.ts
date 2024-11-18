import { computed } from "@vue/reactivity";
import { defineStore } from "pinia";
import { reactive, ref, type Ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useClientStore } from "./client";
import type { AvailabilitySchema, TeamSchema } from "@/client";
import moment, { type Moment } from "moment";
import "moment-timezone";
import { useAuthStore } from "./auth";

export const useScheduleStore = defineStore("schedule", () => {
  const client = useClientStore().client;
  const authStore = useAuthStore();

  const dateStart = ref(moment());

  const windowStart = computed(() => Math.floor(dateStart.value.unix()));

  const availability = reactive(new Array(168));
  availability.fill(0);

  watch(availability, () => {
    // TODO: maybe do not sync these values so that we can cancel editing
    // availability
    let index = playerAvailability.value
      .findIndex((v) => v.steamId == authStore.steamId);
    playerAvailability.value[index].availability = availability;
  });

  const playerAvailability: Ref<AvailabilitySchema[]> = ref([ ]);

  const overlay = computed<number[] | undefined>(() => {
    let members = Object.keys(selectedMembers)
      .filter((x) => selectedMembers[x]);
    if (members.length > 0) {
      const min = Array(168).fill(0);

      const candidates = playerAvailability.value
        .filter((x) => members.includes(x.steamId));
      for (let i = 0; i < 168; i++) {
        min[i] = Math.min(
          ...candidates.map((c) => c.availability ? c.availability[i] : 0));
      }
      //for (const availability of candidates) {
      //}

      return min;
    }

    if (hoveredMember.value) {
      return playerAvailability.value
        .find((x) => x.steamId == hoveredMember.value?.steamId)
        ?.availability;
    }

    return undefined;
  });

  const hoveredMember = ref<AvailabilitySchema>();

  const selectedMembers = reactive<{ [id: string]: boolean }>({ });

  const hoveredIndex: Ref<number | undefined> = ref();

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
    fetchTeamSchedule();
  });

  watch(team, () => {
    dateStart.value = getWindowStart(team.value);
    console.log(dateStart.value);
  });

  async function fetchSchedule(dateStartOverride?: Moment) {
    dateStartOverride = dateStartOverride ?? dateStart.value;
    return client.default.getApiSchedule(
      Math.floor(dateStartOverride.unix()).toString(),
      team.value.id,
    )
      .then((response) => {
        response.availability.forEach((value, i) => {
          availability[i] = value;
        });
        return response;
      });
  }

  async function fetchTeamSchedule(dateStartOverride?: Moment) {
    dateStartOverride = dateStartOverride ?? dateStart.value;
    return client.default.getApiScheduleTeam(
      Math.floor(dateStartOverride.unix()).toString(),
      team.value.id,
    )
      .then((response) => {
        const values = Object.values(response.playerAvailability);
        playerAvailability.value = values;

        let record = values.find((value) => value.steamId == authStore.steamId);

        if (record?.availability) {
          record.availability
            .forEach((value, i) => {
              availability[i] = value;
            });
        }

        return response;
      });
  }

  async function saveSchedule() {
    return client.default.putApiSchedule({
      windowStart: Math.floor(dateStart.value.unix()).toString(),
      teamId: team.value.id,
      availability,
    });
  }

  return {
    dateStart,
    windowStart,
    availability,
    playerAvailability,
    overlay,
    hoveredMember,
    selectedMembers,
    hoveredIndex,
    fetchSchedule,
    fetchTeamSchedule,
    saveSchedule,
    team,
    getWindowStart,
  };
});
