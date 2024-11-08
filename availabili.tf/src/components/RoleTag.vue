<script setup lang="ts">
import { type ViewTeamMembersResponse } from "@/client";
import { useRosterStore } from "../stores/roster";

const rosterStore = useRosterStore();

const props = defineProps({
  role: String,
  player: Object as PropType<ViewTeamMembersResponse>,
});

const roleObject = defineModel();

function toggle(isMain) {
  if (isMain == roleObject.value?.isMain) {
    roleObject.value = undefined;
  } else {
    if (!roleObject.value) {
      // create a new role object
      roleObject.value = {
        role: props.role,
        isMain: isMain
      }
    } else {
      roleObject.value.isMain = isMain;
    }
  }
}
</script>

<template>
  <div class="role">
    <div
      :class="{
        'role-info': true,
        'unselected': !roleObject,
      }"
    >
      <i
        :class="{
          [rosterStore.roleIcons[role]]: true,
        }"
      />
      <span>
        {{ rosterStore.roleNames[role] }}
      </span>
    </div>
    <button
      :class="{
        'center': true,
        'selected': roleObject?.isMain
      }"
      @click="toggle(true)"
    >
      Main
    </button>
    <button
      :class="{
        'right': true,
        'selected': !(roleObject?.isMain ?? true)
      }"
      @click="toggle(false)"
    >
      Alternate
    </button>
  </div>
</template>

<style scoped>
.role {
  display: flex;
}

.role-info {
  width: 100%;
  display: flex;
  align-items: center;
  background-color: var(--mantle);
  gap: 8px;
  padding: 8px 16px;
  border-radius: 8px 0 0 8px;
  font-size: 10pt;
  line-height: 1em;
}

.role-info.unselected {
  color: var(--overlay-0);
}

.role button {
  font-size: 10pt;
  background-color: var(--mantle);
}

.role button.center {
  border-radius: 0;
}

.role button.right {
  border-radius: 0 8px 8px 0;
}

.role button.selected {
  background-color: var(--accent-transparent);
  color: var(--accent);
}

.role i {
  line-height: unset;
  font-size: 12pt;
}
</style>
