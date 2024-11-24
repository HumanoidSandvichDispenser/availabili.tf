import type { EventSchema } from "@/client";
import { defineStore } from "pinia";
import { computed, reactive, ref } from "vue";
import { useClientStore } from "./client";

export const useEventsStore = defineStore("events", () => {
  const clientStore = useClientStore();
  const client = clientStore.client;

  const events = ref<EventSchema[]>([ ]);

  const eventsById = computed(() => {
    return events.value
      .reduce((acc, event) => {
        return { ...acc, [event.id]: event };
      }, { } as { [id: number]: EventSchema });
  });

  function fetchEvent(id: number) {
    return clientStore.call(
      fetchEvent.name,
      () => client.default.getEvent(id),
    );
  }

  return {
    events,
    eventsById,
    fetchEvent,
  }
});
