<script setup lang="ts">
import { useRoute, useRouter, RouterLink, RouterView } from "vue-router";
import { useTeamsStore } from "../stores/teams";
import { computed, onMounted, ref } from "vue";
import { useTeamDetails } from "../composables/team-details";
import MembersList from "../components/MembersList.vue";
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
      <center class="margin">
        <h1>
          {{ team.teamName }}
        </h1>
        <span class="aside">
          Formed on {{ creationDate }}
        </span>
        <div class="icons">
          <RouterLink class="button" :to="'/schedule?teamId=' + team.id">
            <button class="icon" v-tooltip="'Schedule'">
              <i class="bi bi-calendar-fill"></i>
            </button>
          </RouterLink>
          <RouterLink class="button" :to="{ name: 'team-settings/' }">
            <button class="icon" v-tooltip="'Settings'">
              <i class="bi bi-gear-fill"></i>
            </button>
          </RouterLink>
        </div>
      </center>
      <MembersList />
    </template>
  </main>
</template>

<style scoped>
.margin {
  margin: 4em;
}

.icons {
  display: flex;
  justify-content: center;
  margin: 8px;
  gap: 4px;
}

.icons a {
  border-radius: 4px;
}

.icons button {
  color: var(--overlay-0);
  font-size: 12pt;
}

.icons button:hover {
  color: var(--text);
}
</style>
