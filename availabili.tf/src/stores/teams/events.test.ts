import { createPinia, setActivePinia } from "pinia";
import { beforeEach, describe, expect, it } from "vitest";
import { useEventsStore } from "../events";
import { useTeamsEventsStore } from "./events";

describe("Team events store", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  })

  it("should reflect the same events as the events store", () => {
    const eventsStore = useEventsStore();
    eventsStore.events = [
      {
        createdAt: "",
        description: "",
        id: 0,
        name: "test",
        startTime: "",
        teamId: 5,
      },
      {
        createdAt: "",
        description: "",
        id: 2,
        name: "test",
        startTime: "",
        teamId: 5,
      }
    ];

    const teamEventsStore = useTeamsEventsStore();
    const teamEvents = teamEventsStore.teamEvents[5];

    expect(teamEvents.length).toEqual(eventsStore.events.length);
    expect(teamEvents).toEqual(eventsStore.events);
  });
});
