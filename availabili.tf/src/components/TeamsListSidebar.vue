<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useTeamsStore } from "../stores/teams";
import { RouterLink } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import InviteKeyDialog from "./InviteKeyDialog.vue";
import { ContentLoader } from "vue-content-loader";

const teams = useTeamsStore();
const isLoading = ref(false);

const authStore = useAuthStore();

onMounted(() => {
  isLoading.value = true;
  authStore.getUser()
    .then(() => {
      teams.fetchTeams()
        .then(() => {
          isLoading.value = false;
        });
    });
});
</script>

<template>
  <div>
    <div class="teams-header">
      <h2>
        <i class="bi bi-people-fill margin"></i>
        Your Teams
      </h2>
      <div class="button-group" v-if="authStore.isLoggedIn">
        <InviteKeyDialog />
        <RouterLink class="button" to="/team/register">
          <button class="small accent">
            <i class="bi bi-plus-circle-fill margin"></i>
            New
          </button>
        </RouterLink>
      </div>
    </div>
    <div v-if="!authStore.isLoggedIn">
      Log in to view your teams.
    </div>
    <div v-else-if="isLoading || true">
      <ContentLoader :speed="1">
        <circle cx="10" cy="20" r="8" />
        <rect x="25" y="15" rx="5" ry="5" width="220" height="10" />
        <circle cx="10" cy="50" r="8" />
        <rect x="25" y="45" rx="5" ry="5" width="220" height="10" />
        <circle cx="10" cy="80" r="8" />
        <rect x="25" y="75" rx="5" ry="5" width="220" height="10" />
        <circle cx="10" cy="110" r="8" />
        <rect x="25" y="105" rx="5" ry="5" width="220" height="10" />
      </ContentLoader>
    </div>
    <div
      v-else-if="teams.teamsWithRole"
      v-for="(team, _, i) in teams.teamsWithRole"
    >
      <div class="team-item">
        <div class="major-info">
          <RouterLink :to="'/team/id/' + team.id">
            {{ team.teamName }}
          </RouterLink>
          <span class="tag" v-if="team.isTeamLeader">Team Leader</span>
          <span class="tag">{{ teams.roleNames[team.role] }}</span>
        </div>
        <div class="member-info">
          <div class="subtext">
            {{ team.playerCount }} member(s)
          </div>
          <RouterLink
            class="button"
            :to="{ 'name': 'schedule', 'query': { 'teamId': team.id } }"
          >
            <button class="icon" v-tooltip="'View schedule'">
              <i class="bi bi-calendar-fill"></i>
            </button>
          </RouterLink>
        </div>
      </div>
      <hr v-if="i < Object.keys(teams.teams).length - 1" />
    </div>
  </div>
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

.button-group {
  display: flex;
  gap: 0.5rem;
}

.team-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 1rem 0;
}

.team-item a {
  color: var(--text);
  font-size: 1rem;
  font-weight: 600;
}

.tag {
  font-size: 9pt;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  background-color: var(--crust);
}

.team-item .major-info, .team-item .member-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.member-info button.icon {
  color: var(--overlay-0);
}

.member-info button.icon:hover {
  color: var(--text);
}
</style>
