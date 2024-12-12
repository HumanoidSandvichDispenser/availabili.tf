import type { MatchSchema, TeamMatchSchema } from "@/client";
import { defineStore } from "pinia";
import { ref } from "vue";
import { useClientStore } from "./client";

export const useMatchesStore = defineStore("matches", () => {
  const clientStore = useClientStore();
  const client = clientStore.client;

  const matches = ref<{ [id: number]: MatchSchema }>({ });

  const teamMatches = ref<{ [teamId: number]: TeamMatchSchema[] }>({ });

  const recentMatches = ref<TeamMatchSchema[]>([]);

  function fetchMatches() {
    return clientStore.call(
      fetchMatches.name,
      () => client.default.getMatchesForPlayerTeams(),
      (response) => {
        response.forEach((match) => {
          matches.value[match.match.logsTfId] = match.match;
          //teamMatches.value[match.match.logsTfId] = match;
        });
        return response;
      }
    )
  }

  function fetchMatchesForTeam(teamId: number) {
    return clientStore.call(
      fetchMatchesForTeam.name,
      () => client.default.getMatchesForTeam(teamId, 1024),
      (response) => {
        teamMatches.value[teamId] = [];
        response.forEach((match) => {
          matches.value[match.match.logsTfId] = match.match;
          teamMatches.value[teamId].push(match);
        });
        return response;
      });
  }

  function fetchRecentMatchesForTeam(teamId: number, limit: number) {
    return clientStore.call(
      fetchMatchesForTeam.name,
      () => client.default.getMatchesForTeam(teamId, limit),
      (response) => {
        recentMatches.value = [];
        response.forEach((match) => {
          matches.value[match.match.logsTfId] = match.match;
          recentMatches.value.push(match);
        });
        return response;
      });
  }

  function submitMatches(logsTfIds: number[], teamId: number) {
    return client.default.submitMatch({ matchIds: logsTfIds, teamId });
  }

  return {
    matches,
    teamMatches,
    recentMatches,
    fetchMatches,
    fetchMatchesForTeam,
    fetchRecentMatchesForTeam,
    submitMatches,
  }
});
