import type { PlayerRoleSchema } from "@/client";
import { computed, ref } from "vue";
import { useRoute } from "vue-router";

export function useEventForm() {
  const route = useRoute();

  const title = ref("");
  const description = ref<string | null>("");
  const players = ref<PlayerRoleSchema[]>([]);
  const eventId = computed<number | undefined>(() => Number(route.params.eventId));


  return {
    title,
    description,
    players,
    eventId,
  }
}
