<script setup lang="ts">
import { useRoute, useRouter, RouterLink, RouterView } from "vue-router";
import { useTeamsStore } from "../stores/teams";
import { computed, onMounted, ref } from "vue";
import { useTeamDetails } from "../composables/team-details";
import moment from "moment";

const route = useRoute();
const router = useRouter();
const teamsStore = useTeamsStore();
const { team, teamId } = useTeamDetails();

const creationDate = computed(() => {
  if (team.value) {
    return moment(team.value.createdAt).format("L");
  }
});

const key = computed(() => route.query.key);

onMounted(() => {
  let doFetchTeam = () => {
    teamsStore.fetchTeam(teamId.value)
      .then(() => teamsStore.fetchTeamMembers(teamId.value))
      .then(() => teamsStore.getInvites(teamId.value));
  };

  if (key.value) {
    teamsStore.consumeInvite(teamId.value, key.value.toString())
      .finally(doFetchTeam);
  } else {
    doFetchTeam();
  }
});
</script>

<template>
  <main>
    <template v-if="team">
      <center class="team-info">
        <h1>
          {{ team.teamName }}
        </h1>
        <span class="aside">
          Formed on {{ creationDate }}
        </span>
      </center>
      <RouterView />
    </template>
  </main>
</template>

<style scoped>
.team-info {
  margin: 4em;
}
</style>
