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
  <main class="sidebar-container team-settings" v-if="team">
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
        <button class="destructive-on-hover icon-end no-border" @click="leaveTeam">
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
.back-link {
  padding: 8px 16px;
}
</style>
