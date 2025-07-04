<script setup lang="ts">
import type { CancelablePromise, EventSchema } from "@/client";
import { useEventForm } from "@/composables/event-form";
import { useTeamDetails } from "@/composables/team-details";
import { useEventsStore } from "@/stores/events";
import { useRosterStore } from "@/stores/roster";
import { useTeamsStore } from "@/stores/teams";
import moment from "moment";
import { computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();

const rosterStore = useRosterStore();
const teamsStore = useTeamsStore();
const eventsStore = useEventsStore();

const { eventId } = useEventForm();

const { team, teamId } = useTeamDetails();

const startTime = computed(() => {
  if (rosterStore.startTime) {
    return moment.unix(rosterStore.startTime).format("LL LT z");
  }
});

const startTimeTeamTz = computed(() => {
  if (rosterStore.startTime && team.value) {
    // if team timezone is the same as ours, then do nothing
    if (team.value?.tzTimezone === moment.tz.guess()) {
      return undefined;
    }
    return moment.unix(rosterStore.startTime)
      .tz(team.value?.tzTimezone)
      .format("LL LT z");
  }
});

function saveRoster() {
  let promise: CancelablePromise<EventSchema>;

  if (eventId.value) {
    promise = rosterStore.updateRoster(eventId.value);
  } else {
    promise = rosterStore.saveRoster(Number(route.params.teamId));
  }

  promise
    .then((event) => {
      router.push({
        name: "team-details",
        params: {
          id: event.teamId,
        }
      });
    });
}

onMounted(() => {
  if (eventId.value) {
    eventsStore.fetchEvent(eventId.value)
      .then((response) => {
        teamsStore.fetchTeam(response.teamId).then(fetchedTeam => {
          team.value = fetchedTeam;
      });
  }
});
</script>

<template>
  <div class="event-scheduler-container">
    <h1 class="roster-title">
      Roster for {{ team?.teamName }}
    </h1>
    <div v-if="rosterStore.startTime">
      <span class="aside date">
        {{ startTime }}
      </span>
      <br v-if="startTimeTeamTz">
      <span class="aside date">
        {{ startTimeTeamTz }}
      </span>
    </div>
    <div class="form-group margin">
      <h3>Event Name</h3>
      <input v-model="rosterStore.title" />
    </div>
    <div class="form-group margin">
      <h3>Description (optional)</h3>
      <input v-model="rosterStore.description" />
    </div>
    <div class="form-group margin" v-if="!eventId">
      <div>
        <input
          v-model="rosterStore.includePlayersWithoutRoles"
          type="checkbox"
          name="includePlayersWithoutRoles"
        />
        <label for="includePlayersWithoutRoles">
          Include attendance of players without assigned role
        </label>
      </div>
    </div>
    <div class="form-group margin">
      <div class="action-buttons">
        <button class="accent" @click="saveRoster">Save roster</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
em.aside.date {
  font-size: 11pt;
}
</style>
