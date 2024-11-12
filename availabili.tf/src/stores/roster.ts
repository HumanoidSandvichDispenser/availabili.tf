import { type Player, type PlayerTeamRoleFlat } from "@/player";
import { defineStore } from "pinia";
import { computed, reactive, ref, type Reactive, type Ref } from "vue";
import { useClientStore } from "./client";

export const useRosterStore = defineStore("roster", () => {
  const clientStore = useClientStore();
  const client = clientStore.client;

  const neededRoles: Reactive<Array<String>> = reactive([
    "PocketScout",
    "FlankScout",
    "PocketSoldier",
    "Roamer",
    "Demoman",
    "Medic",
  ]);

  const selectedPlayers: Reactive<{ [key: string]: PlayerTeamRoleFlat }> = reactive({});

  const selectedRole: Ref<String | undefined> = ref(undefined);

  const availablePlayers: Ref<Array<PlayerTeamRoleFlat>> = ref([
    {
      steamId: "342534598",
      name: "Wesker U",
      role: "Flank Scout",
      isMain: true,
      availability: 1,
      playtime: 35031,
    },
    {
      steamId: "342534298",
      name: "JustGetAHouse",
      role: "Flank Scout",
      isMain: false,
      availability: 1,
      playtime: 28811,
    },
  ]);

  const availablePlayerRoles = computed(() => {
    return availablePlayers.value.filter((player) => player.role == selectedRole.value);
  });

  const definitelyAvailable = computed(() => {
    return availablePlayerRoles.value.filter((player) => player.availability == 2);
  });

  const canBeAvailable = computed(() => {
    return availablePlayerRoles.value.filter((player) => player.availability == 1);
  });

  function comparator(p1: PlayerTeamRoleFlat, p2: PlayerTeamRoleFlat) {
    // definitely available > can be available
    let availabilityDiff = p1.availability - p2.availability;

    // less playtime is preferred
    let playtimeDiff = p1.playtime - p2.playtime;

    return availabilityDiff || playtimeDiff;
  }

  const mainRoles = computed(() => {
    return availablePlayerRoles.value.filter((player) => player.isMain)
      .sort(comparator);
  });

  const alternateRoles = computed(() => {
    return availablePlayerRoles.value.filter((player) => !player.isMain)
      .sort(comparator);
  });

  const roleIcons = reactive({
    "PocketScout": "tf2-PocketScout",
    "FlankScout": "tf2-FlankScout",
    "PocketSoldier": "tf2-PocketSoldier",
    "Roamer": "tf2-FlankSoldier",
    "Demoman": "tf2-Demo",
    "Medic": "tf2-Medic",
  });

  const roleNames = reactive({
    "PocketScout": "Pocket Scout",
    "FlankScout": "Flank Scout",
    "PocketSoldier": "Pocket Soldier",
    "Roamer": "Roamer",
    "Demoman": "Demoman",
    "Medic": "Medic",
  });

  function selectPlayerForRole(player: PlayerTeamRoleFlat, role: string) {
    if (player && player.steamId) {
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

  function fetchAvailablePlayers(startTime: number, teamId: number) {
    clientStore.call(
      fetchAvailablePlayers.name,
      () => client.default.viewAvailableAtTime(startTime.toString(), teamId),
      (response) => {
        availablePlayers.value = response.players.flatMap((schema) => {
          return schema.roles.map((role) => ({
            steamId: schema.player.steamId,
            name: schema.player.username,
            role: role.role,
            isMain: role.isMain,
            availability: schema.availability,
            playtime: schema.playtime,
          }));
        });

        return response;
      }
    )
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
    roleIcons,
    roleNames,
    mainRoles,
    alternateRoles,
    fetchAvailablePlayers,
  }
});
