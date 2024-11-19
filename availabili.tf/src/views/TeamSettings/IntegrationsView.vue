<script setup lang="ts">
import IntegrationDetails from "@/components/IntegrationDetails.vue";
import { useTeamDetails } from "@/composables/team-details";
import { useTeamsStore } from "@/stores/teams";
import { computed, onMounted, ref } from "vue";

const teamsStore = useTeamsStore();
const {
  teamId,
} = useTeamDetails();

const integrations = computed(() => teamsStore.teamIntegrations[teamId.value]);

function createIntegration() {
  teamsStore.createIntegration(teamId.value, "discord");
}

onMounted(() => {
  teamsStore.fetchTeam(teamId.value)
    .then(() => teamsStore.getIntegrations(teamId.value));
});
</script>

<template>
  <div class="team-integrations">
    <h2>Team Integrations</h2>
    <div v-if="integrations?.length == 0">
      This team currently does not have any integrations.
    </div>
    <div v-else>
      <IntegrationDetails
        v-for="integration in integrations"
        :integration="integration"
      />
    </div>
    <button class="accent" @click="createIntegration">
      <i class="bi bi-database-fill-add margin" />
      Create Integration
    </button>
  </div>
</template>
