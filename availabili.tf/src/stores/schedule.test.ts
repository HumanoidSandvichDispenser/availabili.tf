import { beforeEach, describe, expect, it } from "vitest";
import { useScheduleStore } from "./schedule";
import { createPinia, setActivePinia } from "pinia";

describe("Schedule store", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it("should return the proper window start for any timezone", () => {
    const scheduleStore = useScheduleStore();

    let test1 = scheduleStore.getWindowStart({
      teamName: "",
      id: 0,
      tzTimezone: "Asia/Kolkata",
      minuteOffset: 10,
      createdAt: "",
    });

    expect(test1.get("minutes")).toEqual(40);

    let test2 = scheduleStore.getWindowStart({
      teamName: "",
      id: 0,
      tzTimezone: "America/New_York",
      minuteOffset: 30,
      createdAt: "",
    });

    expect(test2.get("minutes")).toEqual(30);
  });
});
