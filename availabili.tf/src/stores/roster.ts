import { type Player, type PlayerTeamRoleFlat } from "@/player";
import { defineStore } from "pinia";
import { computed, reactive, ref, type Reactive, type Ref } from "vue";
import { useClientStore } from "./client";
import { type EventSchema, type CreateEventJson, type PlayerRoleSchema, type UpdateEventJson } from "@/client";
import { useTeamDetails } from "@/composables/team-details";
import moment from "moment";
import { useRoute, useRouter } from "vue-router";
import { useEventForm } from "@/composables/event-form";

export const useRosterStore = defineStore("roster", () => {
  const clientStore = useClientStore();
  const client = clientStore.client;
  const router = useRouter();
  const route = useRoute();

  // TODO: move roster state to a composable

  const neededRoles  = ref([
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
    "Scout": "Scout",
    "PocketScout": "Pocket Scout",
    "FlankScout": "Flank Scout",
    "Soldier": "Soldier",
    "PocketSoldier": "Pocket Soldier",
    "Roamer": "Roamer",
    "Pyro": "Pyro",
    "Demoman": "Demoman",
    "HeavyWeapons": "Heavy",
    "Engineer": "Engineer",
    "Medic": "Medic",
    "Sniper": "Sniper",
    "Spy": "Spy",
  });

  function selectPlayerForRole(player: PlayerTeamRoleFlat | undefined, role: string) {
    if (player && player.steamId) {
      const existingRole = Object.keys(selectedPlayers).find((selectedRole) => {
        return selectedPlayers[selectedRole]?.steamId == player.steamId &&
          role != selectedRole;
      });

      if (existingRole) {
        delete selectedPlayers[existingRole];
      }
    }

    if (player) {
      selectedPlayers[role] = player;
    } else {
      delete selectedPlayers[role];
    }
  }

  function fetchAvailablePlayers(startTime: number, teamId: number) {
    return clientStore.call(
      fetchAvailablePlayers.name,
      () => client.default.viewAvailableAtTime(startTime.toString(), teamId),
      (response) => {
        availablePlayers.value = response.players
          .flatMap((schema) => {
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

  function fetchPlayersFromEvent(eventId: number) {
    return clientStore.call(
      fetchPlayersFromEvent.name,
      () => client.default.getEventPlayers(eventId),
      (response) => {
        availablePlayers.value = response.players
          .flatMap((schema) => {
            return schema.roles.map((role) => ({
              steamId: schema.player.steamId,
              name: schema.player.username,
              role: role.role,
              isMain: role.isMain,
              availability: schema.hasConfirmed ? 2 : 1,
              playtime: schema.playtime,
            }));
          });

        response.players
          .forEach((schema) => {
            if (schema.role) {
              selectedPlayers[schema.role.role] = {
                steamId: schema.player.steamId,
                name: schema.player.username,
                role: schema.role.role,
                isMain: schema.role.isMain,
                availability: schema.hasConfirmed ? 2 : 1,
                playtime: schema.playtime,
              }
            }
          });

        return response;
      }
    )
  }

  const currentEvent = ref<EventSchema | undefined>(undefined);

  const startTime = ref<number>();

  const { title, description, includePlayersWithoutRoles } = useEventForm();

  function saveRoster(teamId: number) {
    if (startTime.value == undefined) {
      throw new Error("No start time set");
    }

    const body: CreateEventJson = {
      name: title.value,
      description: description.value,
      startTime: startTime.value.toString(),
      includePlayersWithoutRoles: includePlayersWithoutRoles.value,
      playerRoles: Object.values(selectedPlayers).map((player) => ({
        player: {
          steamId: player.steamId,
          username: player.name,
        },
        role: {
          role: player.role,
          isMain: player.isMain,
        },
      })),
    };

    return client.default.createEvent(teamId, body);
  }

  function updateRoster(eventId: number) {
    const body: UpdateEventJson = {
      name: title.value,
      description: description.value,
      playerRoles: Object.values(selectedPlayers).map((player) => ({
        player: {
          steamId: player.steamId,
          username: player.name,
        },
        role: {
          role: player.role,
          isMain: player.isMain,
        },
      })),
    };

    return client.default.updateEvent(eventId, body);
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
    fetchPlayersFromEvent,
    startTime,
    saveRoster,
    updateRoster,
    title,
    description,
    includePlayersWithoutRoles,
  }
});
