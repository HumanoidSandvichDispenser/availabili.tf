import { type Player } from "@/player";
import { defineStore } from "pinia";
import { reactive, ref, type Reactive, type Ref } from "vue";

export const useRosterStore = defineStore("roster", () => {
  const selectedRole: Ref<String | undefined> = ref("Pocket Scout");
  const availablePlayers: Reactive<Array<Player>> = reactive([]);

  return {
    selectedRole,
    availablePlayers,
  }
});
