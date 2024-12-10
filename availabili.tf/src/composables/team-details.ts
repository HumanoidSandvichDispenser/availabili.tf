import { useTeamsStore } from "@/stores/teams";
import { useInvitesStore } from "@/stores/teams/invites";
import { computed } from "vue";
import { useRoute } from "vue-router";

export function useTeamDetails() {
  const route = useRoute();
  const teamsStore = useTeamsStore();
  const invitesStore = useInvitesStore();

  const teamId = computed(() => Number(route.params.id ?? route.params.teamId));

  const team = computed(() => {
    return teamsStore.teams[teamId.value];
  });

  const invites = computed(() => {
    return invitesStore.teamInvites[teamId.value];
  });

  const teamMembers = computed(() => {
    return teamsStore.teamMembers[teamId.value];
  });

  const availableMembers = computed(() => {
    return teamsStore.teamMembers[teamId.value]
      .filter((member) => member.availability[0] > 0);
  });

  const availableMembersNextHour = computed(() => {
    return teamsStore.teamMembers[teamId.value]
      .filter((member) => member.availability[1] > 0);
  });

  return {
    team,
    teamId,
    invites,
    teamMembers,
    availableMembers,
    availableMembersNextHour,
  }
}
