<script setup lang="ts">
import type { PlayerTeamRole } from "../player";
import { computed, type PropType, ref, watch } from "vue";
import { useTeamsStore } from "../stores/teams";
import { useRosterStore } from "../stores/roster";
import { type ViewTeamMembersResponse, type TeamSchema } from "@/client";
import SvgIcon from "@jamescoyle/vue-icon";
import { mdiCrown } from "@mdi/js";
import RoleTag from "../components/RoleTag.vue";

const props = defineProps({
  player: Object as PropType<ViewTeamMembersResponse>,
  team: Object as PropType<TeamSchema>,
});

const teamsStore = useTeamsStore();

const rosterStore = useRosterStore();

//const roles = computed({
//  get: () => ({
//    "PocketScout": "",
//    "FlankScout": "",
//    "PocketSoldier": "",
//    "Roamer": "",
//    "Demoman": "",
//    "Medic": "",
//  }),
//});

const isEditing = ref(false);

// this is the roles of the player we are editing
const roles = ref([]);
const updatedRoles = ref([]);

//const rolesMap = reactive({
//  "Role.PocketScout": undefined,
//  "Role.FlankScout": undefined,
//  "Role.PocketSoldier": undefined,
//  "Role.Roamer": undefined,
//  "Role.Demoman": undefined,
//  "Role.Medic": undefined,
//});

const possibleRoles = [
  "PocketScout",
  "FlankScout",
  "PocketSoldier",
  "Roamer",
  "Demoman",
  "Medic",
];

watch(isEditing, (newValue) => {
  if (newValue) {
    // editing
    roles.value = possibleRoles.map((roleName) => {
      console.log(roleName);
      return props.player.roles
        .find((playerRole) => playerRole.role == roleName) ?? undefined;
    });
  }
});

function updateRoles() {
  isEditing.value = false;
  updatedRoles.value = roles.value.filter(x => x);
  props.player.roles = updatedRoles.value;
  console.log(roles.value);
  console.log(updatedRoles.value);
  teamsStore.updateRoles(props.team.id, props.player.steamId, updatedRoles.value);
}

const isUnavailable = computed(() => {
  return props.player?.availability[0] == 0 &&
    props.player?.availability[1] == 0;
});
</script>

<template>
  <tr class="player-card">
    <td>
      <div
        class="status flex-middle"
        :is-unavailable="isUnavailable"
      >
        <div class="status-indicators">
          <span
            class="indicator left-indicator"
            :availability="player.availability[0]"
          />
          <span
            class="indicator right-indicator"
            :availability="player.availability[1]"
          />
        </div>
        <h3>
          {{ player.username }}
        </h3>
        <svg-icon v-if="player.isTeamLeader" type="mdi" :path="mdiCrown" />
      </div>
    </td>
    <td>
      <div class="role-icons flex-middle">
        <div class="role-buttons" v-if="isEditing">
          <RoleTag
            v-for="role, i in possibleRoles"
            :role="role"
            :player="player"
            v-model="roles[i]"
          />
        </div>
        <template v-else>
          <i
            v-for="role in player.roles"
            :class="{
              [rosterStore.roleIcons[role.role]]: true,
              main: role.isMain,
            }"
          />
        </template>
      </div>
    </td>
    <td>
      {{ player.playtime.toFixed(1) }} hours
    </td>
    <td>
      {{ new Date(player.createdAt).toLocaleString() }}
    </td>
    <td>
      <div class="edit-group">
        <template v-if="isEditing">
          <button class="editing" @click="updateRoles()">
            <i class="bi bi-check-lg" />
          </button>
        </template>
        <button v-else @click="isEditing = true">
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
}

.player-card > td {
  padding: 1em 2em;
}

.player-card h3 {
  font-weight: 600;
  font-size: 12pt;
}

.status-indicators {
  display: flex;
  flex-direction: row;
  gap: 2px;
}

.status-indicators > .indicator {
  display: block;
  height: 8px;
  width: 12px;
  background-color: var(--overlay-0);
}

.left-indicator {
  border-radius: 8px 0 0 8px;
}

.right-indicator {
  border-radius: 0 8px 8px 0;
}

.status[is-unavailable="true"] {
  color: var(--overlay-0);
  font-weight: 400;
}

.status .indicator[availability="1"] {
  background-color: var(--yellow);
}

.status .indicator[availability="2"] {
  background-color: var(--green);
}

.flex-middle {
  display: flex;
  gap: 8px;
  align-items: center;
}

.role-icons i {
  font-size: 24px;
  line-height: 0;
  color: var(--overlay-0);
}

.role-icons i.main {
  color: var(--text);
}

.role-buttons {
  display: flex;
  flex-direction: column;
  gap: 8px;
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

.edit-group > button.editing {
  opacity: 1;
}
</style>
