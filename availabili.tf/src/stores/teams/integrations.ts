import { defineStore } from "pinia";
import { ref } from "vue";
import { useClientStore } from "../client";
import type {
  TeamIntegrationSchema,
  TeamDiscordIntegrationSchema,
  TeamLogsTfIntegrationSchema
} from "@/client";

export const useIntegrationsStore = defineStore("integrations", () => {
  const hasLoaded = ref(false);

  const client = useClientStore().client;

  const discordIntegration = ref<TeamDiscordIntegrationSchema | undefined>();

  const logsTfIntegration = ref<TeamLogsTfIntegrationSchema | undefined>();

  async function getIntegrations(teamId: number) {
    hasLoaded.value = false;
    const response = await client.default.getIntegrations(teamId);
    setIntegrations(response);
    return response;
  }

  function setIntegrations(schema: TeamIntegrationSchema) {
    discordIntegration.value = schema.discordIntegration ?? undefined;
    logsTfIntegration.value = schema.logsTfIntegration ?? undefined;
    hasLoaded.value = true;
  }

  async function updateIntegrations(teamId: number) {
    const body: TeamIntegrationSchema = {
      discordIntegration: discordIntegration.value ?? null,
      logsTfIntegration: logsTfIntegration.value ?? null,
    };
    const response = await client.default.updateIntegrations(teamId, body);
    setIntegrations(response);
    return response;
  }

  return {
    hasLoaded,
    discordIntegration,
    logsTfIntegration,
    getIntegrations,
    updateIntegrations,
  };
});
