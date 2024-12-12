import { defineStore } from "pinia";
import { reactive, type Reactive } from "vue";
import { useClientStore } from "../client";
import { type TeamInviteSchema } from "@/client";

export const useInvitesStore = defineStore("invites", () => {
  const clientStore = useClientStore();
  const client = clientStore.client;

  const teamInvites: Reactive<{ [id: number]: TeamInviteSchema[] }> = reactive({});

  async function getInvites(teamId: number) {
    return clientStore.call(
      getInvites.name,
      () => client.default.getInvites(teamId),
      (response) => {
        teamInvites[teamId] = response;
        return response;
      }
    );
  }

  async function createInvite(teamId: number) {
    const response = await client.default.createInvite(teamId);
    teamInvites[teamId].push(response);
    return response;
  }

  async function consumeInvite(key: string) {
    const response = await client.default.consumeInvite(key);
    const teamId = response.teamId;
    if (teamInvites[teamId]) {
      teamInvites[teamId] = teamInvites[teamId]
        .filter((invite) => invite.key != key);
    }
    return response;
  }

  async function revokeInvite(teamId: number, key: string) {
    const response = await client.default.revokeInvite(teamId, key);
    teamInvites[teamId] = teamInvites[teamId].filter((invite) => invite.key != key);
    return response;
  }

  return {
    teamInvites,
    getInvites,
    createInvite,
    consumeInvite,
    revokeInvite,
  };
});
