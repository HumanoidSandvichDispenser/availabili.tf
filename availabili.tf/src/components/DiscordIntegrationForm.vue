<script setup lang="ts">
import { type TeamDiscordIntegrationSchema } from "@/client";
import { useTeamDetails } from "@/composables/team-details";
import { useIntegrationsStore } from "@/stores/teams/integrations";

const model = defineModel<TeamDiscordIntegrationSchema>();
const integrationsStore = useIntegrationsStore();

const { teamId } = useTeamDetails();

function saveIntegration() {
  integrationsStore.updateIntegrations(teamId.value);
}

function enableIntegration() {
  model.value = {
    webhookUrl: "",
    webhookBotName: "",
    webhookBotProfilePicture: null,
  };
  saveIntegration();
}

function disableIntegration() {
  model.value = undefined;
  saveIntegration();
}
</script>

<template>
  <h2>Discord Webhook</h2>
  <p>Receive notifications in Discord for event updates.</p>
  <div v-if="model">
    <div class="form-group margin">
      <h3>Webhook URL</h3>
      <input v-model="model.webhookUrl">
    </div>
    <div class="form-group margin">
      <h3>Webhook Bot Name</h3>
      <input v-model="model.webhookBotName">
    </div>
    <div class="form-group margin">
      <h3>Webhook Bot Profile Picture URL (optional)</h3>
      <input v-model="model.webhookBotProfilePicture">
    </div>
    <div class="form-group margin">
      <div class="action-buttons">
        <button class="destructive-on-hover" @click="disableIntegration">
          <i class="bi bi-trash" />
          Disable integration
        </button>
        <button class="accent" @click="saveIntegration">
          <i class="bi bi-check" />
          Save
        </button>
      </div>
    </div>
  </div>
  <div v-else>
    <button class="accent" @click="enableIntegration">
      <i class="bi bi-check" />
      Enable Discord Integration
    </button>
  </div>
</template>
