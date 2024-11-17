<script setup lang="ts">
import { useTeamsStore } from "../stores/teams";
import { useRoute, useRouter, RouterLink } from "vue-router";
import { computed } from "vue";
import { useTeamDetails } from "../composables/team-details";
import PlayerTeamCard from "../components/PlayerTeamCard.vue";

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

function leaveTeam() {
  teamsStore.leaveTeam(team.value.id)
    .then(() => {
      teamsStore.fetchTeams()
        .then(() => {
          router.push("/");
        })
    });
}
</script>

<template>
  <div class="member-list-header">
    <h2>
      <i class="bi bi-people-fill margin" />
      Members
    </h2>
    <em class="aside" v-if="teamMembers">
      {{ teamMembers?.length }} member(s),
      {{ availableMembers?.length }} currently available,
      {{ availableMembersNextHour?.length }} available in the next hour
    </em>
    <div class="team-details-button-group">
    </div>
  </div>
  <table class="member-table">
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

table.member-table th {
  text-align: left;
  padding-left: 2em;
  font-weight: 700;
}

.team-details-button-group {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: end;
  gap: 4px;
}
</style>
