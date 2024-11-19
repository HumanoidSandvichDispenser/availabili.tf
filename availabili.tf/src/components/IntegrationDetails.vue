<script setup lang="ts">
import type { TeamIntegrationSchema, TeamDiscordIntegrationSchema } from "@/client";
import { useTeamDetails } from "@/composables/team-details";
import { useTeamsStore } from "@/stores/teams";
import { computed } from "vue";

const props = defineProps<{
  integration: TeamIntegrationSchema,
}>();

const teamsStore = useTeamsStore();

const { teamId } = useTeamDetails();

/*
const isDiscord = (x: TeamIntegrationSchema): x is TeamDiscordIntegrationSchema => x.integrationType === "team_discord_integrations";

const isDiscordIntegration = computed(() => {
  return isDiscord(props.integration);
});
*/

const discordIntegration = computed(() => props.integration as TeamDiscordIntegrationSchema);

function deleteIntegration() {
  teamsStore.deleteIntegration(teamId.value, props.integration.id);
}

function saveIntegration() {
  teamsStore.updateIntegration(teamId.value, props.integration);
}
</script>

<template>
  <details class="accordion">
    <summary>
      <span class="title">
        <h2 v-if="discordIntegration">
          Discord Integration
        </h2>
        <span class="aside">(id: {{ props.integration.id }})</span>
      </span>
    </summary>

    <div class="form-group margin">
      <h3>Webhook URL</h3>
      <input v-model="discordIntegration.webhookUrl" />
    </div>

    <div class="button-group">
      <button class="destructive-on-hover" @click="deleteIntegration">
        <i class="bi bi-trash margin" />
        Delete
      </button>
      <button @click="saveIntegration">Save</button>
    </div>
  </details>
</template>

<style scoped>
.button-group {
  display: flex;
  gap: 4px;
  justify-content: end;
}

summary > .title {
  display: flex;
  align-items: center;
  gap: 0.5em;
}

summary .aside {
  font-size: 1rem;
}
</style>
