<script setup lang="ts">
import { useRoute, useRouter, RouterLink } from "vue-router";
import { useTeamsStore } from "../stores/teams";
import { computed, onMounted } from "vue";
import PlayerTeamCard from "../components/PlayerTeamCard.vue";

const route = useRoute();
const router = useRouter();
const teamsStore = useTeamsStore();

const team = computed(() => {
  return teamsStore.teams[route.params.id];
});

const availableMembers = computed(() => {
  return teamsStore.teamMembers[route.params.id]
    .filter((member) => member.availability > 0);
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
        {{ team.teamName }}
        <RouterLink :to="'/schedule?teamId=' + team.id">
          <button class="accent">
            <i class="bi bi-calendar-fill margin"></i>
            View schedule
          </button>
        </RouterLink>
        <em class="aside" v-if="teamsStore.teamMembers[route.params.id]">
          {{ teamsStore.teamMembers[route.params.id]?.length }} member(s),
          {{ availableMembers?.length }} currently available
        </em>
      </h1>
      <table class="member-table">
        <!--thead>
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
        </thead-->
        <tbody>
          <PlayerTeamCard
            v-for="member in teamsStore.teamMembers[route.params.id]"
            :player="member"
            :team="team"
            :key="member.username"
          />
        </tbody>
      </table>
    </template>
  </main>
</template>

<style scoped>
h1 {
  display: flex;
  gap: 0.5em;
  align-items: center;
}

h1 > em.aside {
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

/*
div.member-grid {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
*/
</style>
