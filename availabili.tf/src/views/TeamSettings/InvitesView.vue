<script setup lang="ts">
import { useTeamDetails } from "@/composables/team-details";
import { useTeamsStore } from "@/stores/teams";
import { onMounted } from "vue";
import InviteEntry from "@/components/InviteEntry.vue";

const teamsStore = useTeamsStore();

const {
  team,
  teamId,
  invites,
} = useTeamDetails();

function createInvite() {
  teamsStore.createInvite(team.value.id);
}

onMounted(() => {
  teamsStore.fetchTeam(teamId.value)
    .then(() => teamsStore.getInvites(teamId.value));
});
</script>

<template>
  <div class="invites" v-if="team">
    <table id="invite-table" v-if="invites?.length > 0">
      <thead>
        <tr>
          <th>
            Key (hover to reveal)
          </th>
          <th>
            Creation time
          </th>
        </tr>
      </thead>
      <tbody>
        <InviteEntry
          v-for="invite in invites"
          :invite="invite"
        />
      </tbody>
    </table>
    <div class="create-invite-group">
      <button class="accent" @click="createInvite">
        <i class="bi bi-person-fill-add margin" />
        Create Invite
      </button>
      <span class="small aside">
        Invites are usable once and expire after 24 hours.
      </span>
    </div>
  </div>
</template>

<style scoped>
#invite-table {
  width: 100%;
  border: 1px solid var(--overlay-0);
  border-radius: 8px;
  margin: 8px 0;
}

#invite-table th {
  text-align: left;
  font-weight: 600;
  padding: 8px;
}

</style>
