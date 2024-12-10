import type { MatchSchema, TeamMatchSchema } from "@/client";
import { defineStore } from "pinia";
import { ref } from "vue";
import { useClientStore } from "./client";

export const useMatchesStore = defineStore("matches", () => {
  const clientStore = useClientStore();
  const client = clientStore.client;

  const matches = ref<{ [id: number]: MatchSchema }>({ });

  const teamMatches = ref<{ [id: number]: TeamMatchSchema }>({ });

  function fetchMatches() {
    return clientStore.call(
      fetchMatches.name,
      () => client.default.getMatchesForPlayerTeams(),
      (response) => {
        response.forEach((match) => {
          matches.value[match.match.logsTfId] = match.match;
          teamMatches.value[match.match.logsTfId] = match;
        });
        return response;
      }
    )
  }

  function submitMatches(logsTfIds: number[]) {
    return client.default.submitMatch({ matchIds: logsTfIds });
  }

  return {
    matches,
    teamMatches,
    fetchMatches,
    submitMatches,
  }
});
