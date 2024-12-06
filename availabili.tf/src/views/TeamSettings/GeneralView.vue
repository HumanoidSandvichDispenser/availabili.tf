<script setup lang="ts">
import { useTeamSettings } from "@/composables/team-settings";
import timezones from "@/assets/timezones.json";
import { onMounted, ref } from "vue";
import { useTeamsStore } from "@/stores/teams";
import { useTeamDetails } from "@/composables/team-details";
import { computed } from "@vue/reactivity";

const {
  teamName,
  timezone,
  minuteOffset,
} = useTeamSettings();

const { teamId } = useTeamDetails();

function updateTeamSettings() {
  teamsStore.updateTeam(teamId.value, {
    teamName: teamName.value,
    leagueTimezone: timezone.value,
    minuteOffset: minuteOffset.value,
  });
}

function resetChanges() {
  teamName.value = team.value.teamName;
  timezone.value = team.value.tzTimezone;
  minuteOffset.value = team.value.minuteOffset;
}

const hasChangedDetails = computed(() => {
  if (!team) {
    return false;
  }

  return (
    teamName.value !== team.value.teamName ||
    timezone.value !== team.value.tzTimezone ||
    minuteOffset.value !== team.value.minuteOffset
  );
});

const hasChangedTimeDetails = computed(() => {
  if (!team) {
    return false;
  }

  return (
    timezone.value !== team.value.tzTimezone ||
    minuteOffset.value !== team.value.minuteOffset
  );
});

const isLoaded = ref(false);

const teamsStore = useTeamsStore();

const team = computed(() => teamsStore.teams[teamId.value]);

onMounted(() => {
  isLoaded.value = true;
  teamsStore.fetchTeam(teamId.value)
    .then((response) => {
      teamName.value = response.team.teamName;
      timezone.value = response.team.tzTimezone;
      minuteOffset.value = response.team.minuteOffset;
      isLoaded.value = false;
    });
})
</script>

<template>
  <div class="team-general-settings">
    <h2>Overview</h2>
    <div>
      <div class="form-group margin">
        <h3 class="closer">Team Name</h3>
        <input v-model="teamName" />
      </div>
      <div class="form-group margin">
        <div class="form-group row">
          <div class="form-group">
            <h3>
              Timezone
              <a
                class="aside"
                href="https://nodatime.org/TimeZones"
                target="_blank"
              >
                (view all timezones)
              </a>
            </h3>
            <v-select :options="timezones" v-model="timezone" />
          </div>
          <div class="form-group" id="minute-offset-group">
            <h3>Minute Offset</h3>
            <input type="number" v-model="minuteOffset" min="0" max="59" />
          </div>
        </div>
        <em class="aside">
          Matches will be scheduled based on {{ timezone }} at
          {{ minuteOffset }}
          <span v-if="minuteOffset == 1">
            minute
          </span>
          <span v-else>
            minutes
          </span>
          past the hour.
        </em>
      </div>
      <div class="form-group margin" v-if="hasChangedTimeDetails">
        <div class="banner warning">
          <i class="bi bi-exclamation-triangle-fill margin"></i>
          Warning: changing the timezone or minute offset will remove all
          current availability data.
        </div>
      </div>
      <div class="form-group margin">
        <div class="action-buttons">
          <button class="transparent" v-if="hasChangedDetails" @click="resetChanges">
            <i class="bi bi-arrow-counterclockwise"></i>
            Undo changes
          </button>
          <button class="accent" @click="updateTeamSettings">Save</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>
