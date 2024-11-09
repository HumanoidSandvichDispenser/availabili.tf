<script setup lang="ts">
import { type TeamInviteSchema } from "../client";
import { useTeamsStore } from "../stores/teams";
import { computed } from "vue";

const teamsStore = useTeamsStore();

const props = defineProps({
  invite: Object as PropType<TeamInviteSchema>,
});

const inviteLink = computed(() => {
  let teamId = props.invite.teamId;
  let key = props.invite.key;
  return `${window.location.origin}/team/id/${teamId}?key=${key}`;
})

function copyLink() {
  navigator.clipboard.writeText(inviteLink.value);
}

function revokeInvite() {
  teamsStore.revokeInvite(props.invite.teamId, props.invite.key);
}
</script>

<template>
  <tr>
    <td>
      <a class="key" :href="inviteLink">
        <code>
          {{ invite.key }}
        </code>
      </a>
    </td>
    <td>
      {{ invite.createdAt }}
    </td>
    <td class="buttons">
      <button @click="copyLink">
        <i class="bi bi-link margin" />
        Copy Link
      </button>
      <button class="destructive" @click="revokeInvite">
        <i class="bi bi-trash margin" />
        Revoke
      </button>
    </td>
  </tr>
</template>

<style scoped>
tr .buttons {
  opacity: 0;
  transition-duration: 200ms;
}

tr:hover .buttons {
  opacity: 1;
}

td {
  padding: 8px;
}

.key {
  color: var(--text);
  background-color: var(--text);
  padding: 2px 4px;
}

.key:hover {
  color: var(--base);
  transition-duration: 200ms;
}

.buttons {
  display: flex;
  align-content: center;
  justify-content: end;
  gap: 8px;
}
</style>
