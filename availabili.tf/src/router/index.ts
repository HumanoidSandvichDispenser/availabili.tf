import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import ScheduleView from "../views/ScheduleView.vue";
import RosterBuilderView from "../views/RosterBuilderView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView
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
  ]
})

export default router
