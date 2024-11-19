import { defineStore } from "pinia";
import { reactive, type Reactive } from "vue";
import { useClientStore } from "../client";
import { type TeamIntegrationSchema, type AbstractTeamIntegrationSchema } from "@/client";

export const useIntegrationsStore = defineStore("integrations", () => {
  const clientStore = useClientStore();
  const client = clientStore.client;

  const teamIntegrations = reactive<{ [id: number]: TeamIntegrationSchema[] }>({});

  async function getIntegrations(teamId: number) {
    const response = await client.default.getIntegrations(teamId.toString());
    teamIntegrations[teamId] = response;
    return response;
  }

  async function createIntegration(teamId: number, integrationType: string) {
    const response = await client.default.createIntegration(teamId.toString(), integrationType);
    teamIntegrations[teamId].push(response);
    return response;
  }

  async function deleteIntegration(teamId: number, integrationId: number) {
    const response = await client.default.deleteIntegration(teamId.toString(), integrationId.toString());
    teamIntegrations[teamId] = teamIntegrations[teamId].filter((integration) => integration.id != integrationId);
    return response;
  }

  async function updateIntegration(teamId: number, integration: AbstractTeamIntegrationSchema) {
    const response = await client.default.updateIntegration(teamId.toString(), integration.id.toString(), integration);
    const index = teamIntegrations[teamId].findIndex((x) => x.id == integration.id);
    teamIntegrations[teamId][index] = response;
    return response;
  }

  return {
    teamIntegrations,
    getIntegrations,
    createIntegration,
    deleteIntegration,
    updateIntegration,
  };
});
