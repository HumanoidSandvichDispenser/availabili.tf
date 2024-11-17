import { ref, watch } from "vue";

export function useTeamSettings() {
  const teamName = ref("");

  const timezone = ref(
    Intl.DateTimeFormat().resolvedOptions().timeZone ??
      "Etc/UTC"
  );

  const minuteOffset = ref(0);

  watch(minuteOffset, (newValue) => {
    minuteOffset.value = Math.min(Math.max(0, newValue), 59);
  });

  return {
    teamName,
    timezone,
    minuteOffset,
  }
}
