<script setup lang="ts">
import { useTeamDetails } from "@/composables/team-details";
import { useTeamsStore } from "@/stores/teams";
import { onMounted } from "vue";
import InviteEntry from "@/components/InviteEntry.vue";
import { useInvitesStore } from "@/stores/teams/invites";

const teamsStore = useTeamsStore();
const invitesStore = useInvitesStore();

const {
  team,
  teamId,
  invites,
} = useTeamDetails();

function createInvite() {
  invitesStore.createInvite(team.value.id);
}

onMounted(() => {
  teamsStore.fetchTeam(teamId.value)
    .then(() => invitesStore.getInvites(teamId.value));
});
</script>

<template>
  <div class="invites" v-if="team">
    <h2>Invites</h2>
    <p class="small aside">
      Invite players to your team by creating an invite link.
      All invites are usable only once.
    </p>
    <div class="create-invite-group">
      <button class="accent" @click="createInvite">
        <i class="bi bi-person-fill-add margin" />
        Create Invite
      </button>
    </div>
    <table id="invite-table" v-if="invites?.length > 0">
      <thead>
        <tr>
          <th>
            Key (hover to reveal)
          </th>
          <th>
            Creation time
          </th>
          <th>
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
  </div>
</template>

<style scoped>
#invite-table {
  width: 100%;
  border-radius: 8px;
  margin: 8px 0;
}

#invite-table th {
  text-align: left;
  font-weight: 600;
  padding: 8px;
}

.create-invite-group {
  display: flex;
  gap: 8px;
  align-items: center;
  justify-content: end;
}
</style>
