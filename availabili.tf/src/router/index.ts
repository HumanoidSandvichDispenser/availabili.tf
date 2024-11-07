import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import ScheduleView from "../views/ScheduleView.vue";
import RosterBuilderView from "../views/RosterBuilderView.vue";
import LoginView from "../views/LoginView.vue";
import TeamRegistrationView from "../views/TeamRegistrationView.vue";
import TeamDetailsView from "../views/TeamDetailsView.vue";

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
      path: "/schedule/roster",
      name: "roster-builder",
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
      component: TeamDetailsView
    },
  ]
})

export default router
