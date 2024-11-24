import { defineStore } from "pinia";
import { useClientStore } from "../client";
import type { EventSchema, EventSchemaList } from "@/client";
import { useEventsStore } from "../events";
import { computed } from "vue";

export const useTeamsEventsStore = defineStore("teamsEvents", () => {
  const clientStore = useClientStore();
  const client = clientStore.client;
  const eventsStore = useEventsStore();

  const teamEvents = computed(() => {
    console.log("Recomputing teamEvents");

    // map events to objects with teamId as key, and array of events as value
    return eventsStore.events
      .reduce((acc, event) => {
        if (!acc[event.teamId]) {
          acc[event.teamId] = [];
        }
        acc[event.teamId].push(event);
        return acc;
      }, { } as { [teamId: number]: EventSchema[] });
  });

  function fetchTeamEvents(teamId: number) {
    return clientStore.call(
      fetchTeamEvents.name,
      () => client.default.getTeamEvents(teamId),
      (result: EventSchemaList) => {
        result.forEach((event) => {
          // insert into event store
          //eventsStore.events[event.id] = event;
          eventsStore.events.push(event);
        });
        return result;
      }
    );
  }

  return {
    teamEvents,
    fetchTeamEvents,
  }
});
