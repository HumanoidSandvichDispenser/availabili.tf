import Cacheable from "@/cacheable";
import { AvailabilitfClient, type RoleSchema, type TeamSpec, type ViewTeamMembersResponse, type ViewTeamResponse, type ViewTeamsResponse } from "@/client";
import { defineStore } from "pinia";
import { computed, reactive, ref, type Reactive, type Ref } from "vue";
import { useClientStore } from "./client";

export type TeamMap = { [id: number]: TeamSpec };

export const useTeamsStore = defineStore("teams", () => {
  const clientStore = useClientStore();
  const client = clientStore.client;

  const teams: Reactive<{ [id: number]: TeamSpec }> = reactive({ });
  const teamMembers: Reactive<{ [id: number]: ViewTeamMembersResponse[] }> = reactive({ });

  const isFetchingTeams = ref(false);

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

  async function createTeam(teamName: string, tz: string, webhook?: string) {
    return await client.default.createTeam({
      teamName,
      leagueTimezone: tz,
      discordWebhookUrl: webhook,
    });
  }

  async function updateRoles(teamId: number, playerId: number, roles: RoleSchema[]) {
    return await client.default
      .editMemberRoles(teamId.toString(), playerId.toString(), {
        roles,
      });
  }

  return {
    teams,
    teamMembers,
    fetchTeams,
    fetchTeam,
    fetchTeamMembers,
    createTeam,
    updateRoles
  };
});
