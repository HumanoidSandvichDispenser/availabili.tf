import { ref } from "vue";

export function useTeamSettings() {
  const teamName = ref("");

  const timezone = ref(
    Intl.DateTimeFormat().resolvedOptions().timeZone ??
      "Etc/UTC"
  );
}
