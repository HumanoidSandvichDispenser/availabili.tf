<script setup lang="ts">
import { useEventForm } from "@/composables/event-form";
import { useTeamDetails } from "@/composables/team-details";
import { useRosterStore } from "@/stores/roster";
import { useTeamsStore } from "@/stores/teams";
import moment from "moment";
import { computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();

const rosterStore = useRosterStore();
const teamsStore = useTeamsStore();

const { eventId } = useEventForm();

const { team, teamId } = useTeamDetails();

const startTime = computed(() => {
  if (rosterStore.startTime) {
    return moment.unix(rosterStore.startTime).format("LL LT z");
  }
});

const startTimeTeamTz = computed(() => {
  if (rosterStore.startTime) {
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
  if (eventId.value) {
    rosterStore.updateRoster(eventId.value);
  } else {
    rosterStore.saveRoster(Number(route.params.teamId))
      .then(() => {
        router.push({
          name: "team-details",
          params: {
            id: route.params.teamId
          }
        });
      });
  }
}

onMounted(() => {
  if (!team.value) {
    teamsStore.fetchTeam(teamId.value);
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
