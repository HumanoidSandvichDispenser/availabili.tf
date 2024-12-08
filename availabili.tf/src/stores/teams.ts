import { defineStore } from "pinia";
import { reactive, type Reactive } from "vue";
import { useClientStore } from "./client";
import { useAuthStore } from "./auth";
import { type TeamSchema, type RoleSchema, type ViewTeamMembersResponse, type CreateTeamJson, type TeamWithRoleSchema } from "@/client";

export type TeamMap = { [id: number]: TeamSchema };

export const useTeamsStore = defineStore("teams", () => {
  const authStore = useAuthStore();
  const clientStore = useClientStore();
  const client = clientStore.client;

  const teams = reactive<{ [id: number]: TeamSchema }>({});
  const teamsWithRole = reactive<{ [id: number]: TeamWithRoleSchema }>({});
  const teamMembers = reactive<{ [id: number]: ViewTeamMembersResponse[] }>({});

  const roleNames: { [key: string]: string } = {
    "Player": "Player",
    "CoachMentor": "Coach/Mentor",
  };

  async function fetchTeams() {
    const response = await clientStore.call(
      fetchTeams.name,
      () => client.default.getTeams()
    );
    response.teams.forEach((team) => {
      teams[team.id] = team;
      teamsWithRole[team.id] = team;
    });
    return response;
  }

  async function fetchTeam(id: number) {
    const response = await clientStore.call(
      fetchTeam.name,
      () => client.default.getTeam(id.toString())
    );
    teams[response.team.id] = response.team;
    return response;
  }

  async function fetchTeamMembers(id: number) {
    const response = await clientStore.call(
      fetchTeamMembers.name,
      () => client.default.getTeamMembers(id.toString())
    );
    teamMembers[id] = response.map((member): ViewTeamMembersResponse => {
      member.roles = member.roles.sort((a, b) => (a.isMain === b.isMain ? 0 : a.isMain ? -1 : 1));
      return member;
    });
    console.log(teamMembers[id]);
    return teamMembers[id];
  }

  async function createTeam(teamName: string, tz: string, minuteOffset: number) {
    return await client.default.createTeam({
      teamName,
      leagueTimezone: tz,
      minuteOffset,
    });
  }

  async function updateTeam(teamId: number, args: CreateTeamJson) {
    return await client.default.updateTeam(teamId, args)
      .then((response) => teams[teamId] = response);
  }

  async function updateRoles(teamId: number, playerId: string, roles: RoleSchema[]) {
    return await client.default.editMemberRoles(teamId.toString(), playerId, { roles });
  }

  async function leaveTeam(teamId: number) {
    return client.default.removePlayerFromTeam(teamId.toString(), authStore.steamId);
  }

  return {
    teams,
    teamsWithRole,
    roleNames,
    teamMembers,
    fetchTeams,
    fetchTeam,
    fetchTeamMembers,
    createTeam,
    updateTeam,
    updateRoles,
    leaveTeam,
  };
});
