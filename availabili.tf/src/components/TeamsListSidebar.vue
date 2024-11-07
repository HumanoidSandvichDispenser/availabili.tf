<script setup lang="ts">
import { onMounted } from "vue";
import { useTeamsStore } from "../stores/teams";
import { RouterLink } from "vue-router";

const teams = useTeamsStore();

onMounted(() => {
  teams.fetchTeams();
});
</script>

<template>
  <aside>
    <div>
      <div class="teams-header">
        <h3>Your Teams</h3>
        <RouterLink to="/team/register">
          <button class="small accent">
            <i class="bi bi-plus-circle-fill margin"></i>
            New
          </button>
        </RouterLink>
      </div>
      <div
        v-if="teams.teams"
        v-for="team in teams.teams"
      >
        <RouterLink :to="'/team/id/' + team.id">
          {{ team.team_name }}
        </RouterLink>
      </div>
    </div>
  </aside>
</template>

<style scoped>
aside {
  flex-basis: 256px;
}

.teams-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.teams-header h3 {
  font-weight: 600;
}
</style>
