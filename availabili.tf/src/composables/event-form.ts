import type { PlayerRoleSchema } from "@/client";
import { ref } from "vue";

export function useEventForm() {
  const title = ref("");
  const description = ref("");
  const players = ref<PlayerRoleSchema[]>([]);

  return {
    title,
    description,
    players,
  }
}
