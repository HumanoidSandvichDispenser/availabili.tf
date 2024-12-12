<script setup lang="ts">
import { type TeamLogsTfIntegrationSchema } from "@/client";
import { useTeamDetails } from "@/composables/team-details";
import { useIntegrationsStore } from "@/stores/teams/integrations";

const model = defineModel<TeamLogsTfIntegrationSchema>();
const integrationsStore = useIntegrationsStore();

const { teamId } = useTeamDetails();

function saveIntegration() {
  integrationsStore.updateIntegrations(teamId.value);
}

function enableIntegration() {
  model.value = {
    logsTfApiKey: "",
    minTeamMemberCount: 4,
  };
  integrationsStore.updateIntegrations(teamId.value);
}

function disableIntegration() {
  model.value = undefined;
  integrationsStore.updateIntegrations(teamId.value);
}
</script>

<template>
  <h2>logs.tf Auto-Tracking</h2>
  <p>Automatically fetch and track match history from logs.tf.</p>
  <div v-if="model">
    <div class="form-group margin">
      <h3>logs.tf API key (optional)</h3>
      <input v-model="model.logsTfApiKey">
    </div>
    <div class="form-group margin">
      <h3>Minimum Team Members</h3>
      <p>
        Minimum number of team members needed to appear in the logs.tf match to
        automatically be included in the team match history.
      </p>
      <input v-model="model.minTeamMemberCount" type="number">
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
      Enable logs.tf Integration
    </button>
  </div>
</template>
