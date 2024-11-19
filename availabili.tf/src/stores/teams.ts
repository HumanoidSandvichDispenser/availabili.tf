import Cacheable from "@/cacheable";
import { AvailabilitfClient, type TeamInviteSchema, type RoleSchema, type TeamSchema, type ViewTeamMembersResponse, type ViewTeamResponse, type ViewTeamsResponse, type TeamIntegrationSchema, type AbstractTeamIntegrationSchema } from "@/client";
import { defineStore } from "pinia";
import { computed, reactive, ref, type Reactive, type Ref } from "vue";
import { useClientStore } from "./client";
import { useAuthStore } from "./auth";
import moment from "moment";

export type TeamMap = { [id: number]: TeamSchema };

export const useTeamsStore = defineStore("teams", () => {
  const authStore = useAuthStore();

  const clientStore = useClientStore();
  const client = clientStore.client;

  const teams: Reactive<{ [id: number]: TeamSchema }> = reactive({ });
  const teamMembers: Reactive<{ [id: number]: ViewTeamMembersResponse[] }> = reactive({ });
  const teamInvites: Reactive<{ [id: number]: TeamInviteSchema[] }> = reactive({ });
  const teamIntegrations = reactive<{ [id: number]: TeamIntegrationSchema[] }>({ });

  async function fetchTeams() {
    return clientStore.call(
      fetchTeams.name,
      () => client.default.getTeams(),
      (response) => {
        response.teams.forEach((team) => {
          teams[team.id] = team;
        });
        return response;
      }
    )
  }

  async function fetchTeam(id: number) {
    return clientStore.call(
      fetchTeam.name,
      () => client.default.getTeam(id.toString()),
      (response) => {
        teams[response.team.id] = response.team;
        return response;
      }
    );
  }

  async function fetchTeamMembers(id: number) {
    return clientStore.call(
      fetchTeam.name,
      () => client.default.getTeamMembers(id.toString()),
      (response) => {
        response = response
          .map((member): ViewTeamMembersResponse => {
            // TODO: snake_case to camelCase
            member.roles = member.roles
              .sort((a, b) => {
                if (a.isMain == b.isMain) {
                  return 0;
                }
                return a.isMain ? -1 : 1;
              });
            return member;
          });
        console.log(response);
        teamMembers[id] = response;
        return response;
      }
    );
  }

  async function createTeam(teamName: string, tz: string, minuteOffset: number) {
    return await client.default.createTeam({
      teamName,
      leagueTimezone: tz,
      minuteOffset,
    });
  }

  async function updateRoles(teamId: number, playerId: string, roles: RoleSchema[]) {
    return await client.default
      .editMemberRoles(teamId.toString(), playerId, {
        roles,
      });
  }

  async function getInvites(teamId: number) {
    return clientStore.call(
      getInvites.name,
      () => client.default.getInvites(teamId.toString()),
      (response) => {
        teamInvites[teamId] = response;
        return response;
      }
    );
  }

  async function createInvite(teamId: number) {
    return client.default.createInvite(teamId.toString())
      .then((response) => {
        teamInvites[teamId].push(response);
        return response;
      })
  }

  async function consumeInvite(teamId: number, key: string) {
    return client.default.consumeInvite(teamId.toString(), key)
      .then((response) => {
        teamInvites[teamId] = teamInvites[teamId]
          .filter((invite) => invite.key != key);
        return response;
      });
  }

  async function revokeInvite(teamId: number, key: string) {
    return client.default.revokeInvite(teamId.toString(), key)
      .then((response) => {
        teamInvites[teamId] = teamInvites[teamId]
          .filter((invite) => invite.key != key);
        return response;
      });
  }

  async function getIntegrations(teamId: number) {
    return client.default.getIntegrations(teamId.toString())
      .then((response) => {
        teamIntegrations[teamId] = response;
        return response;
      });
  }

  async function createIntegration(teamId: number, integrationType: string) {
    return client.default
      .createIntegration(teamId.toString(), integrationType)
      .then((response) => {
        teamIntegrations[teamId].push(response);
        return response;
      });
  }

  async function deleteIntegration(teamId: number, integrationId: number) {
    return client.default
      .deleteIntegration(teamId.toString(), integrationId.toString())
      .then((response) => {
        teamIntegrations[teamId] = teamIntegrations[teamId]
          .filter((integration) => integration.id != integrationId);
        return response;
      });
  }

  async function updateIntegration(
    teamId: number,
    integration: AbstractTeamIntegrationSchema,
  ) {
    return client.default
      .updateIntegration(teamId.toString(), integration.id.toString(), integration)
      .then((response) => {
        const index = teamIntegrations[teamId]
          .findIndex((x) => x.id == integration.id);
        teamIntegrations[teamId][index] = response;
        return response;
      });
  }

  async function leaveTeam(teamId: number) {
    return client.default
      .removePlayerFromTeam(teamId.toString(), authStore.steamId);
  }

  return {
    teams,
    teamInvites,
    teamMembers,
    fetchTeams,
    fetchTeam,
    fetchTeamMembers,
    createTeam,
    updateRoles,
    getInvites,
    createInvite,
    consumeInvite,
    revokeInvite,
    leaveTeam,
    // TODO: move to separate store
    teamIntegrations,
    getIntegrations,
    createIntegration,
    deleteIntegration,
    updateIntegration,
  };
});
