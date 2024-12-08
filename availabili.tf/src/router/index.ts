import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import ScheduleView from "../views/ScheduleView.vue";
import RosterBuilderView from "../views/RosterBuilderView.vue";
import LoginView from "../views/LoginView.vue";
import TeamRegistrationView from "../views/TeamRegistrationView.vue";
import TeamDetailsView from "../views/TeamDetailsView.vue";
import { useAuthStore } from "@/stores/auth";
//import TeamDetailsMembersListView from "../views/TeamDetailsMembersListView.vue";
import TeamSettingsView from "@/views/TeamSettingsView.vue";
import TeamSettingsGeneralView from "@/views/TeamSettings/GeneralView.vue";
import TeamSettingsIntegrationsView from "@/views/TeamSettings/IntegrationsView.vue";
import TeamSettingsInvitesView from "@/views/TeamSettings/InvitesView.vue";
import UserSettingsView from "@/views/UserSettingsView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView
    },
    {
      path: "/login",
      name: "login",
      component: LoginView
    },
    {
      path: "/schedule",
      name: "schedule",
      component: ScheduleView
    },
    {
      path: "/schedule/roster/:teamId/:startTime",
      name: "roster-builder",
      component: RosterBuilderView
    },
    {
      path: "/schedule/roster/event/:eventId",
      name: "roster-builder-event",
      component: RosterBuilderView
    },
    {
      path: "/team/register",
      name: "team-registration",
      component: TeamRegistrationView
    },
    {
      path: "/team/id/:id",
      name: "team-details",
      component: TeamDetailsView,
    },
    {
      path: "/team/id/:id/settings",
      name: "team-settings",
      component: TeamSettingsView,
      children: [
        {
          path: "",
          name: "team-settings/",
          component: TeamSettingsGeneralView,
        },
        {
          path: "integrations",
          name: "team-settings/integrations",
          component: TeamSettingsIntegrationsView,
        },
        {
          path: "invites",
          name: "team-settings/invites",
          component: TeamSettingsInvitesView,
        },
      ],
    },
    {
      path: "/settings",
      name: "user-settings",
      component: UserSettingsView,
    },
  ]
});

router
  .beforeEach(async (to, from) => {
    const authStore = useAuthStore();
    console.log("test");
    if (!authStore.isLoggedIn && !authStore.hasCheckedAuth) {
      if (to.name != "login") {
        try {
          await authStore.getUser();
        } catch (exception) {

        }
      }
    }
  });

export default router;
