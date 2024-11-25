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

  const availablePlayers: Ref<Array<PlayerTeamRoleFlat>> = ref([ ]);

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

  const roleIcons = reactive<{ [key: string]: string }>({
    "Scout": "tf2-Scout",
    "PocketScout": "tf2-PocketScout",
    "FlankScout": "tf2-FlankScout",
    "Soldier": "tf2-Soldier",
    "PocketSoldier": "tf2-PocketSoldier",
    "Roamer": "tf2-FlankSoldier",
    "Pyro": "tf2-Pyro",
    "Demoman": "tf2-Demo",
    "HeavyWeapons": "tf2-Heavy",
    "Engineer": "tf2-Engineer",
    "Medic": "tf2-Medic",
    "Sniper": "tf2-Sniper",
    "Spy": "tf2-Spy",
  });

  const roleNames = reactive<{ [key: string]: string }>({
    "Scout": "Scout (HL)",
    "PocketScout": "Pocket Scout (6s)",
    "FlankScout": "Flank Scout (6s)",
    "Soldier": "Soldier (HL)",
    "PocketSoldier": "Pocket Soldier (6s)",
    "Roamer": "Roamer (6s)",
    "Pyro": "Pyro",
    "Demoman": "Demoman",
    "HeavyWeapons": "Heavy",
    "Engineer": "Engineer",
    "Medic": "Medic",
    "Sniper": "Sniper",
    "Spy": "Spy",
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
