<script setup lang="ts">
import type { PlayerEventRolesSchema } from "@/client";
import { useRosterStore } from "@/stores/roster";
import {
  DropdownMenuRoot,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuPortal,
  DropdownMenuRadioItem,
  DropdownMenuRadioGroup,
  DropdownMenuItemIndicator,
} from "radix-vue";
import { computed } from "vue";

const rosterStore = useRosterStore();

const props = defineProps<{
  playerEvent: PlayerEventRolesSchema | null;
}>();

const emit = defineEmits<{
  attend: [],
  unattend: [],
  pending: [],
}>();

function attendOrUnattend() {
  if (props.playerEvent?.hasConfirmed) {
    emit("unattend");
  } else {
    emit("attend");
  }
}

const confirmationOptions = ["Attending", "Pending", "Not attending"];

const selectedOption = computed({
  get() {
    if (props.playerEvent?.hasConfirmed) {
      return "Attending";
    } else if (props.playerEvent?.hasConfirmed === false) {
      return "Pending";
    } else {
      return "Not attending";
    }
  },
  set(value: string) {
    console.log(value);
    if (value === "Attending") {
      emit("attend");
    } else if (value === "Not attending") {
      emit("unattend");
    } else {
      emit("pending");
    }
  },
});
</script>

<template>
  <div
    :class="{
      'event-confirm-button': true,
      'confirmed': playerEvent?.hasConfirmed,
    }"
  >
    <button
      @click="attendOrUnattend()"
      v-if="playerEvent"
      class="class-info left recolor"
    >
      <template v-if="!playerEvent.hasConfirmed">
        <i class="bi bi-check2" />
        Confirm
      </template>
      <template v-else>
        <i class="bi bi-check2-all" />
        Attending
      </template>
      <span v-if="playerEvent.role">
        as {{ rosterStore.roleNames[playerEvent.role.role] }}
      </span>
    </button>
    <button v-else @click="emit('attend')" class="left">
      <i class="bi bi-check2" />
      Attend
    </button>
    <DropdownMenuRoot>
      <DropdownMenuTrigger className="right recolor">
        <i class="bi bi-caret-down-fill" />
      </DropdownMenuTrigger>
      <DropdownMenuPortal>
        <DropdownMenuContent>
          <DropdownMenuRadioGroup v-model="selectedOption">
            <DropdownMenuRadioItem
              v-for="option in confirmationOptions"
              as="button"
              :value="option"
            >
              <DropdownMenuItemIndicator>
                <i class="bi bi-check" />
              </DropdownMenuItemIndicator>
              {{ option }}
            </DropdownMenuRadioItem>
          </DropdownMenuRadioGroup>
        </DropdownMenuContent>
      </DropdownMenuPortal>
    </DropdownMenuRoot>
  </div>
</template>

<style scoped>
.event-confirm-button {
  display: flex;
  gap: 2px;
}

.left {
  border-radius: 4px 0 0 4px;
}

.right {
  border-radius: 0 4px 4px 0;
  padding: 6px 12px;
}

.confirmed button.recolor {
  background-color: var(--text);
  color: var(--base);
}
</style>
