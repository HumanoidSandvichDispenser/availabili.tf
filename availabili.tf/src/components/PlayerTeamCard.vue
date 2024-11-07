<script setup lang="ts">
import type { PlayerTeamRole } from "../player";
import { computed, type PropType } from "vue";
import { useRosterStore } from "../stores/roster";
import { type ViewTeamMembersResponse } from "@/client";

const props = defineProps({
  player: Object as PropType<ViewTeamMembersResponse>,
});

const rosterStore = useRosterStore();
</script>

<template>
  <tr class="player-card">
    <td>
      <div class="status flex-middle" :availability="player.availability">
        <span class="dot"></span>
        <h3>
          {{ player.username }}
        </h3>
      </div>
    </td>
    <td>
      <div class="role-icons flex-middle">
        <i
          v-for="role in player.roles"
          :class="{
            [rosterStore.roleIcons[role.role]]: true,
            main: role.is_main,
          }"
        />
      </div>
    </td>
    <td>
      {{ player.playtime.toFixed(1) }} hours
    </td>
    <td>
      {{ new Date(player.created_at).toLocaleString() }}
    </td>
    <td>
      <div class="edit-group">
        <button>
          <i class="bi bi-pencil-fill edit-icon" />
        </button>
      </div>
    </td>
  </tr>
</template>

<style scoped>
.player-card {
  border-radius: 8px;
  user-select: none;
  gap: 1em;
  align-items: center;
  border: 2px solid white;
  box-shadow: 1px 1px 8px var(--surface-0);
}

.player-card > td {
  padding: 1em 2em;
}

.player-card h3 {
  font-weight: 600;
  font-size: 12pt;
}

.dot {
  display: block;
  border-radius: 50%;
  height: 8px;
  width: 8px;
  background-color: var(--overlay-0);
}

.status[availability="0"] h3 {
  color: var(--overlay-0);
  font-weight: 400;
}

.status[availability="1"] .dot {
  background-color: var(--yellow);
}

.status[availability="2"] .dot {
  background-color: var(--green);
}

.flex-middle {
  display: flex;
  gap: 8px;
  align-items: center;
}

.role-icons {
  font-size: 24px;
  line-height: 0;
  color: var(--overlay-0);
}

.role-icons i.main {
  color: var(--text);
}

.edit-group {
  display: flex;
  justify-content: end;
}

.edit-group > button {
  background-color: transparent;
  opacity: 0;
  padding: 8px;
}

.edit-group > button:hover {
  background-color: var(--surface-0);
}

.player-card:hover .edit-group > button {
  opacity: 1;
}
</style>
