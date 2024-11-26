<script setup lang="ts">
import DiscordIntegrationForm from "@/components/DiscordIntegrationForm.vue";
import IntegrationDetails from "@/components/IntegrationDetails.vue";
import LogsTfIntegrationForm from "@/components/LogsTfIntegrationForm.vue";
import { useTeamDetails } from "@/composables/team-details";
import { useTeamsStore } from "@/stores/teams";
import { useIntegrationsStore } from "@/stores/teams/integrations";
import { computed, onMounted, ref } from "vue";

const teamsStore = useTeamsStore();
const integrationsStore = useIntegrationsStore();
const { teamId } = useTeamDetails();

//function createIntegration() {
//  integrationsStore.createIntegration(teamId.value, "discord");
//}

onMounted(() => {
  teamsStore.fetchTeam(teamId.value)
    .then(() => integrationsStore.getIntegrations(teamId.value));
});
</script>

<template>
  <div class="team-integrations">
    <DiscordIntegrationForm v-model="integrationsStore.discordIntegration" />
    <LogsTfIntegrationForm v-model="integrationsStore.logsTfIntegration" />
  </div>
</template>

<style scoped>
.team-integrations {
  display: flex;
  flex-direction: column;
  gap: 1em;
}
</style>
