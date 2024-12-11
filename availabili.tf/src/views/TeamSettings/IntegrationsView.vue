<script setup lang="ts">
import DiscordIntegrationForm from "@/components/DiscordIntegrationForm.vue";
import LoaderContainer from "@/components/LoaderContainer.vue";
import LogsTfIntegrationForm from "@/components/LogsTfIntegrationForm.vue";
import { useTeamDetails } from "@/composables/team-details";
import { useTeamsStore } from "@/stores/teams";
import { useIntegrationsStore } from "@/stores/teams/integrations";
import { onMounted, ref } from "vue";

const teamsStore = useTeamsStore();
const integrationsStore = useIntegrationsStore();
const { teamId } = useTeamDetails();

const isLoading = ref(false);

//function createIntegration() {
//  integrationsStore.createIntegration(teamId.value, "discord");
//}

onMounted(() => {
  isLoading.value = true;
  teamsStore.fetchTeam(teamId.value)
    .then(() => {
      integrationsStore.getIntegrations(teamId.value)
        .then(() => {
          isLoading.value = false;
        });
    });
});
</script>

<template>
  <div class="team-integrations">
    <div v-if="isLoading">
      <LoaderContainer />
    </div>
    <template v-else>
      <DiscordIntegrationForm v-model="integrationsStore.discordIntegration" />
      <LogsTfIntegrationForm v-model="integrationsStore.logsTfIntegration" />
    </template>
  </div>
</template>

<style scoped>
.team-integrations {
  display: flex;
  flex-direction: column;
  gap: 1em;
}
</style>
