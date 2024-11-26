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
    const response = await client.default.getIntegrations(teamId.toString());
    setIntegrations(response);
    return response;
  }

  function setIntegrations(schema: TeamIntegrationSchema) {
    discordIntegration.value = schema.discordIntegration;
    logsTfIntegration.value = schema.logsTfIntegration;
    hasLoaded.value = true;
  }

  async function updateIntegrations(teamId: number) {
    const body: TeamIntegrationSchema = {
      discordIntegration: discordIntegration.value,
      logsTfIntegration: logsTfIntegration.value,
    };
    const response = await client.default.updateIntegrations(teamId.toString(), body);
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
