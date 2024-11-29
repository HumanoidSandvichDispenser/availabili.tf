import { defineStore } from "pinia";
import { useClientStore } from "../client";
import type { EventWithPlayerSchema } from "@/client";
import { useEventsStore } from "../events";
import { computed, reactive } from "vue";

export const useTeamsEventsStore = defineStore("teamsEvents", () => {
  const clientStore = useClientStore();
  const client = clientStore.client;
  //const eventsStore = useEventsStore();

  const teamEvents = reactive<{ [teamId: number]: EventWithPlayerSchema[] }>({ });
  //const teamEvents = computed(() => {
  //  console.log("Recomputing teamEvents");

  //  // map events to objects with teamId as key, and array of events as value
  //  return eventsStore.events
  //    .reduce((acc, event) => {
  //      if (!acc[event.teamId]) {
  //        acc[event.teamId] = [];
  //      }
  //      acc[event.teamId].push(event);
  //      return acc;
  //    }, { } as { [teamId: number]: EventSchema[] });
  //});

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

  function attendEvent(eventId: number) {
    client.default.attendEvent(eventId)
      .then((response) => {
        let index = teamEvents[response.event.teamId]
          .findIndex((event) => event.event.id == response.event.id);
        teamEvents[response.event.teamId][index] = response;
      });
  }

  function unattendEvent(eventId: number) {
    client.default.unattendEvent(eventId)
      .then((response) => {
        let index = teamEvents[response.event.teamId]
          .findIndex((event) => event.event.id == response.event.id);
        teamEvents[response.event.teamId][index].playerEvent = null;
      });
  }

  return {
    teamEvents,
    fetchTeamEvents,
    attendEvent,
    unattendEvent,
  }
});
