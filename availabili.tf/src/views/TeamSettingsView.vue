<script setup lang="ts">
import { useTeamsStore } from "@/stores/teams";
import { useTeamDetails } from "@/composables/team-details";
import { onMounted } from "vue";
import { RouterLink, RouterView, useRouter } from "vue-router";

const teamsStore = useTeamsStore();
const router = useRouter();

const {
  team,
  teamId,
} = useTeamDetails();

function leaveTeam() {
  teamsStore.leaveTeam(teamId.value)
    .then(() => router.push("/"));
}

onMounted(() => {
  teamsStore.fetchTeam(teamId.value);
});
</script>

<template>
  <main class="team-settings" v-if="team">
    <nav class="sidebar">
      <div class="categories">
        <div class="back-link">
          <RouterLink :to="{ name: 'team-details' }">
            <i class="bi bi-arrow-left-short" />
            {{ team.teamName }}
          </RouterLink>
        </div>
        <h3>Settings</h3>
        <RouterLink class="tab" :to="{ name: 'team-settings/' }">
          Overview
        </RouterLink>
        <RouterLink class="tab" :to="{ name: 'team-settings/integrations' }">
          Integrations
        </RouterLink>
        <RouterLink class="tab" :to="{ name: 'team-settings/invites' }">
          Invites
        </RouterLink>
        <RouterLink class="tab" :to="{ name: 'team-settings/matches' }">
          Matches
        </RouterLink>
        <hr>
        <button class="destructive-on-hover icon-end" @click="leaveTeam">
          Leave team
          <i class="bi bi-box-arrow-left" />
        </button>
      </div>
    </nav>
    <div class="view">
      <RouterView />
    </div>
  </main>
</template>

<style scoped>
.team-settings {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.team-settings nav.sidebar {
  display: flex;
  justify-content: end;
}

.team-settings .view {
  width: 60%;
}

.back-link {
  padding: 8px 16px;
}

nav.sidebar h3 {
  text-transform: uppercase;
  color: var(--overlay-0);
  padding: 0 8px;
  font-size: 8pt;
}

nav.sidebar > .categories {
  display: flex;
  flex-direction: column;
  width: 192px;
  gap: 4px;
}

nav.sidebar a.tab {
  font-size: 11pt;
  color: var(--overlay-0);
  padding: 6px 10px;
  font-weight: 500;
  border-radius: 4px;
}

nav.sidebar a.tab:hover {
  background-color: var(--crust);
  color: var(--text);
}

nav.sidebar a.tab.router-link-exact-active {
  background-color: var(--crust);
  color: var(--text);
}

nav.sidebar button {
  font-size: 11pt;
  font-weight: 500;
  padding: 6px 10px;
  background-color: transparent;
  color: var(--overlay-0);
}

nav.sidebar button:hover {
  background-color: var(--crust);
  color: var(--text);
}
</style>
