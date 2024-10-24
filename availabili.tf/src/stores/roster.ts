import { type Player, type PlayerTeamRole } from "@/player";
import { defineStore } from "pinia";
import { computed, reactive, ref, type Reactive, type Ref } from "vue";

export const useRosterStore = defineStore("roster", () => {
  const neededRoles: Reactive<Array<String>> = reactive([
    "Pocket Scout",
    "Flank Scout",
    "Pocket Soldier",
    "Roamer",
    "Demoman",
    "Medic",
  ]);

  const selectedPlayers: Reactive<{ [key: string]: PlayerTeamRole }> = reactive({});

  const selectedRole: Ref<String | undefined> = ref("Pocket Scout");

  const availablePlayers: Reactive<Array<PlayerTeamRole>> = reactive([
    {
      steamId: 2840,
      name: "Wesker U",
      role: "Flank Scout",
      main: true,
      availability: 1,
    },
    {
      steamId: 2839,
      name: "JustGetAHouse",
      role: "Flank Scout",
      main: false,
      availability: 1,
    },
    {
      steamId: 2839,
      name: "JustGetAHouse",
      role: "Pocket Scout",
      main: true,
      availability: 1,
    },
    {
      steamId: 2841,
      name: "VADIKUS007",
      role: "Pocket Soldier",
      main: true,
      availability: 2,
    },
    {
      steamId: 2841,
      name: "VADIKUS007",
      role: "Roamer",
      main: false,
      availability: 2,
    },
    {
      steamId: 2282,
      name: "Bergman777",
      role: "Demoman",
      main: true,
      availability: 2,
    },
    {
      steamId: 2842,
      name: "BossOfThisGym",
      role: "Roamer",
      main: false,
      availability: 2,
    },
    {
      steamId: 2842,
      name: "BossOfThisGym",
      role: "Demoman",
      main: false,
      availability: 2,
    },
    {
      steamId: 2842,
      name: "BossOfThisGym",
      role: "Pocket Scout",
      main: false,
      availability: 2,
    },
    //{
    //  steamId: 2843,
    //  name: "samme1g",
    //  role: "Medic",
    //  main: true,
    //  availability: 2,
    //},
    {
      steamId: 2843,
      name: "samme1g",
      role: "Pocket Soldier",
      main: false,
      availability: 2,
    },
    {
      steamId: 2843,
      name: "samme1g",
      role: "Roamer",
      main: false,
      availability: 2,
    },
    {
      steamId: 2844,
      name: "FarbrorBarbro",
      role: "Roamer",
      main: true,
      availability: 1,
    },
    {
      steamId: 2844,
      name: "FarbrorBarbro",
      role: "Pocket Soldier",
      main: false,
      availability: 1,
    },
  ]);

  const availablePlayerRoles = computed(() => {
    return availablePlayers.filter((player) => player.role == selectedRole.value);
  });

  const definitelyAvailable = computed(() => {
    return availablePlayerRoles.value.filter((player) => player.availability == 2);
  });

  const canBeAvailable = computed(() => {
    return availablePlayerRoles.value.filter((player) => player.availability == 1);
  });

  function selectPlayerForRole(player: PlayerTeamRole, role: string) {
    console.log("selecting.");
    if (player) {
      const existingRole = Object.keys(selectedPlayers).find((selectedRole) => {
        return selectedPlayers[selectedRole]?.steamId == player.steamId &&
          role != selectedRole;
      });

      if (existingRole) {
        delete selectedPlayers[existingRole];
      }
    }

    selectedPlayers[role] = player;
  }

  return {
    neededRoles,
    selectedPlayers,
    selectedRole,
    availablePlayers,
    availablePlayerRoles,
    selectPlayerForRole,
    definitelyAvailable,
    canBeAvailable,
  }
});
