import { defineStore } from "pinia";
import { useClientStore } from "../client";
import type { EventWithPlayerSchema } from "@/client";
import { useEventsStore } from "../events";
import { computed, reactive } from "vue";

export const useTeamsEventsStore = defineStore("teamsEvents", () => {
  const clientStore = useClientStore();
  const client = clientStore.client;

  const teamEvents = reactive<{ [teamId: number]: EventWithPlayerSchema[] }>({ });

  function fetchTeamEvents(teamId: number) {
    return clientStore.call(
      fetchTeamEvents.name,
      () => client.default.getTeamEvents(teamId),
      (result: EventWithPlayerSchema[]) => {
        teamEvents[teamId] = result;
        return result;
      }
    );
  }

  async function attendEvent(eventId: number) {
    return client.default.attendEvent(eventId)
      .then((response) => {
        let index = teamEvents[response.event.teamId]
          .findIndex((event) => event.event.id == response.event.id);
        teamEvents[response.event.teamId][index] = response;
      });
  }

  async function unattendEvent(eventId: number) {
    return client.default.unattendEvent(eventId)
      .then((response) => {
        let index = teamEvents[response.event.teamId]
          .findIndex((event) => event.event.id == response.event.id);
        teamEvents[response.event.teamId][index].playerEvent = null;
      });
  }

  async function deleteEvent(eventId: number) {
    return client.default.deleteEvent(eventId)
      .then(() => {

      });
  }

  return {
    teamEvents,
    fetchTeamEvents,
    deleteEvent,
    attendEvent,
    unattendEvent,
  }
});
