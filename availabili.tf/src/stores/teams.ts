import Cacheable from "@/cacheable";
import { defineStore } from "pinia";
import { computed, reactive, ref, type Reactive, type Ref } from "vue";

interface Team {
  id: number,
  teamName: string,
}

export const useTeamsStore = defineStore("teams", () => {
  //const teams: Reactive<Cacheable<Team[]>> =
  //  reactive(new Cacheable<Team[]>([], 0));
  const teams: Ref<{ [id: number]: Team }> = ref({ });

  async function fetchTeams() {
    return new Promise((res, rej) => {
      fetch(import.meta.env.VITE_API_BASE_URL + "/team/view", {
        credentials: "include",
      })
        .then((response) => response.json())
        .then((response: Array<any>) => {
          teams.value = response
            .reduce((acc, team: Team) => {
              return { ...acc, [team.id]: team }
            });
          res(teams.value);
        })
        .catch(() => rej());
    });
  }

  return {
    teams,
    fetchTeams,
  }
});
