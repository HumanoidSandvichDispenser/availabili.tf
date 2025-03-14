<script setup lang="ts">
import { computed, type PropType, ref, watch } from "vue";
import { useTeamsStore } from "../stores/teams";
import { useRosterStore } from "../stores/roster";
import { type ViewTeamMembersResponse, type TeamSchema, type RoleSchema } from "@/client";
// @ts-expect-error
import SvgIcon from "@jamescoyle/vue-icon";
import { mdiCrown } from "@mdi/js";
import RoleTag from "../components/RoleTag.vue";
import moment from "moment";

const props = defineProps({
  player: {
    type: Object as PropType<ViewTeamMembersResponse>,
    required: true,
  },
  team: {
    type: Object as PropType<TeamSchema>,
    required: true,
  },
});

const teamsStore = useTeamsStore();

const rosterStore = useRosterStore();

const isEditing = ref(false);

// this is the roles of the player we are editing
const roles = ref<(RoleSchema | undefined)[]>([]);
const updatedRoles = ref<RoleSchema[]>([]);

const possibleRoles = [
  "Scout",
  "PocketScout",
  "FlankScout",
  "Soldier",
  "Pyro",
  "PocketSoldier",
  "Roamer",
  "Demoman",
  "HeavyWeapons",
  "Engineer",
  "Medic",
  "Sniper",
  "Spy",
];

watch(isEditing, (newValue) => {
  if (newValue) {
    // editing
    roles.value = possibleRoles
      .map((roleName) => {
        console.log(roleName);
        return props.player.roles
          .find((playerRole) => playerRole.role == roleName) ?? undefined;
      });
  }
});

function updateRoles() {
  isEditing.value = false;
  updatedRoles.value = roles.value.filter((x): x is RoleSchema => !!x);
  props.player.roles = updatedRoles.value;
  console.log(roles.value);
  console.log(updatedRoles.value);
  teamsStore.updateRoles(props.team.id, props.player.steamId, updatedRoles.value);
}

function cancelEdit() {
  isEditing.value = false;
}

const isUnavailable = computed(() => {
  return props.player?.availability[0] == 0 &&
    props.player?.availability[1] == 0;
});

const nextHour = computed(() => {
  const now = moment();
  const time = now.clone().tz(props.team.tzTimezone);

  let minute = time.minute();
  let minuteOffset = props.team.minuteOffset;
  if (minute >= minuteOffset) {
    time.add(1, "hour");
  }
  time.minute(minuteOffset);

  const diff = time.utc().diff(now, "minutes", false);

  return `${diff} minute(s) (${time.local().format("LT")})`;
});

const leftIndicator = computed(() => {
  switch (props.player?.availability[0]) {
    case 0:
      return "Not currently available";
    case 1:
      return "Currently available if needed";
    case 2:
      return "Currently available";
  }
});

const rightIndicator = computed(() => {
  switch (props.player?.availability[1]) {
    case 0:
      return `Not available in ${nextHour.value}`;
    case 1:
      return `Available if needed in ${nextHour.value}`;
    case 2:
      return `Available in ${nextHour.value}`;
  }
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
            v-tooltip="leftIndicator"
            :availability="player.availability[0]"
          />
          <span
            class="indicator right-indicator"
            v-tooltip="rightIndicator"
            :availability="player.availability[1]"
          />
        </div>
        <a
          class="player-name"
          :href="`https://steamcommunity.com/profiles/${player.steamId}`"
        >
          <h3>
            {{ player.username }}
          </h3>
        </a>
        <svg-icon
          v-if="player.isTeamLeader"
          :class="[
            isUnavailable ? '' : 'crown',
          ]"
          type="mdi"
          :path="mdiCrown"
        />
      </div>
    </td>
    <td :colspan="isEditing ? 2 : 1">
      <div class="role-icons flex-middle">
        <div class="role-buttons" v-if="isEditing">
          <RoleTag
            v-for="role, i in possibleRoles"
            :role="role"
            :player="player"
            v-model="roles[i]"
          />
        </div>
        <template v-else-if="player.roles.length > 0">
          <div
            class="role-icon"
            v-for="role in player.roles"
            v-tooltip="rosterStore.roleNames[role.role]"
          >
            <i
              :class="{
                [rosterStore.roleIcons[role.role]]: true,
                main: role.isMain,
              }"
            />
          </div>
        </template>
        <span v-else class="aside">
          No roles
        </span>
        <div class="edit-group">
          <button v-if="!isEditing" class="icon" @click="isEditing = true">
            <i class="bi bi-pencil-fill edit-icon" />
          </button>
        </div>
      </div>
    </td>
    <td v-if="!isEditing">
      <span :class="{ 'aside': player.playtime == 0}">
        {{ player.playtime.toFixed(1) }} hours
      </span>
    </td>
    <!--td>
      {{ new Date(player.createdAt).toLocaleString() }}
    </td-->
    <td>
      <div class="edit-group">
        <template v-if="isEditing">
          <button class="editing icon" @click="cancelEdit()">
            <i class="bi bi-x-lg" />
          </button>
          <button class="editing icon" @click="updateRoles()">
            <i class="bi bi-check-lg" />
          </button>
        </template>
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
  padding: 0.5em 1em;
}

.player-card h3 {
  font-weight: 600;
  font-size: 12pt;
}

.player-card .crown {
  color: var(--yellow);
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

a.player-name {
  color: unset;
}

a.player-name:hover {
  background-color: unset;
}

.flex-middle {
  display: flex;
  gap: 8px;
  align-items: center;
}

.role-icons > .role-icon i {
  font-size: 24px;
  line-height: 1;
  color: var(--overlay-0);
  vertical-align: middle;
}

.role-icons > .role-icon i.main {
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

@media (max-width: 1024px) {
  .player-card > td {
    padding: 0.5em 0em;
  }
}
</style>
