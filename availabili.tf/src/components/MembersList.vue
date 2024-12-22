<script setup lang="ts">
import { useTeamsStore } from "../stores/teams";
import { useRoute, useRouter, RouterLink } from "vue-router";
import { computed, onMounted, ref } from "vue";
import { useTeamDetails } from "../composables/team-details";
import PlayerTeamCard from "../components/PlayerTeamCard.vue";
import LoaderContainer from "./LoaderContainer.vue";

const route = useRoute();
const router = useRouter();
const teamsStore = useTeamsStore();
const {
  team,
  invites,
  availableMembers,
  availableMembersNextHour,
  teamMembers,
} = useTeamDetails();
const isLoading = ref(false);

onMounted(() => {
  isLoading.value = true;
  teamsStore.fetchTeamMembers(team.value.id)
    .finally(() => isLoading.value = false);
});
</script>

<template>
  <div class="member-list-header">
    <h2>
      <i class="bi bi-people-fill margin" />
      Members
    </h2>
    <em class="aside" v-if="teamMembers">
      {{ teamMembers?.length }} member(s)
    </em>
    <div class="team-details-button-group">
    </div>
  </div>
  <LoaderContainer v-if="isLoading">
    <rect x="0" y="10" rx="3" ry="3" width="100%" height="10" />
    <rect x="0" y="30" rx="3" ry="3" width="100%" height="10" />
    <rect x="0" y="50" rx="3" ry="3" width="100%" height="10" />
    <rect x="0" y="70" rx="3" ry="3" width="100%" height="10" />
  </LoaderContainer>
  <table class="member-table" v-else>
    <thead>
      <tr>
        <th>Username</th>
        <th>Roles</th>
        <th>Playtime</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <PlayerTeamCard
        v-for="member in teamMembers"
        :player="member"
        :team="team"
        :key="member.username"
      />
    </tbody>
  </table>
</template>

<style scoped>
.member-list-header {
  display: flex;
  gap: 0.5em;
  align-items: center;
}

.member-list-header > .aside {
  font-size: 12pt;
  font-style: normal;
}

table.member-table {
  width: 100%;
}

.team-details-button-group {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: end;
  gap: 4px;
}
</style>
