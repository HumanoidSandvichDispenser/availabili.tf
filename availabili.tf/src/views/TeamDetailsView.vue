<script setup lang="ts">
import { useRoute, useRouter } from "vue-router";
import { useTeamsStore } from "../stores/teams";
import { computed, onMounted } from "vue";
import PlayerTeamCard from "../components/PlayerTeamCard.vue";

const route = useRoute();
const router = useRouter();
const teamsStore = useTeamsStore();

const team = computed(() => {
  return teamsStore.teams[route.params.id];
});

onMounted(() => {
  teamsStore.fetchTeam(route.params.id)
    .then(() => teamsStore.fetchTeamMembers(route.params.id));
});
</script>

<template>
  <main>
    <template v-if="team">
      <h1>
        {{ team.team_name }}
      </h1>
      <table class="member-table">
        <thead>
          <tr>
            <th>
              Name
            </th>
            <th>
              Roles
            </th>
            <th>
              Playtime on team
            </th>
            <th>
              Joined
            </th>
          </tr>
        </thead>
        <tbody>
          <PlayerTeamCard
            v-for="member in teamsStore.teamMembers[route.params.id]"
            :player="member"
          />
        </tbody>
      </table>
    </template>
  </main>
</template>

<style scoped>
h1 {
  display: flex;
}

table.member-table {
  width: 100%;
}

table.member-table th {
  text-align: left;
  padding-left: 2em;
  font-weight: 700;
}

/*
div.member-grid {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
*/
</style>
