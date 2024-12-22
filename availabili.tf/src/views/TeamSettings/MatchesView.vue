<script setup lang="ts">
import AddMatchDialog from "@/components/AddMatchDialog.vue";
import { useTeamDetails } from "@/composables/team-details";
import { useMatchesStore } from "@/stores/matches";
import { useTeamsStore } from "@/stores/teams";
import moment from "moment";
import { computed, onMounted } from "vue";

const matchesStore = useMatchesStore();
const teamsStore = useTeamsStore();

const { team, teamId } = useTeamDetails();

const matches = computed(() => matchesStore.teamMatches[teamId.value]);

onMounted(() => {
  teamsStore.fetchTeam(teamId.value)
    .then(() => matchesStore.fetchMatchesForTeam(teamId.value));
});
</script>

<template>
  <div class="header">
    <h2>
      <i class="bi bi-trophy-fill margin"></i>
      Matches
    </h2>
  </div>
  <div class="button-group">
    <AddMatchDialog />
  </div>
  <table>
    <thead>
      <tr>
        <th>RED</th>
        <th>BLU</th>
        <th>Team</th>
        <th>Match Date</th>
        <th>logs.tf URL</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="teamMatch in matches">
        <td>{{ teamMatch.match.redScore }}</td>
        <td>{{ teamMatch.match.blueScore }}</td>
        <td>{{ teamMatch.teamColor == 'Blue' ? 'BLU' : 'RED' }}</td>
        <td>{{ moment(teamMatch.match.matchTime).format("LL LT") }}</td>
        <td>
          <a :href="`https://logs.tf/${teamMatch.match.logsTfId}`" target="_blank">
            #{{ teamMatch.match.logsTfId }}
          </a>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.button-group {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 0.5rem;
}

table {
  width: 100%;
}
</style>
