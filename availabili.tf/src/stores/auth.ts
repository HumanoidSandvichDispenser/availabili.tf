import { defineStore } from "pinia";
import { ref } from "vue";

export const useAuthStore = defineStore("auth", () => {
  const steamId = ref(NaN);
  const username = ref("");
  const isLoggedIn = ref(false);
  const isRegistering = ref(false);

  async function login(queryParams: { [key: string]: string }) {
    return fetch(import.meta.env.VITE_API_BASE_URL + "/login/authenticate", {
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "same-origin",
      method: "POST",
      body: JSON.stringify(queryParams),
    })
      .then((response) => response.json())
      .then((response) => {
        isRegistering.value = response.isRegistering;
        if (!isRegistering.value) {
          steamId.value = response.steamId;
          username.value = response.username;
          isLoggedIn.value = true;
          isRegistering.value = false;
        }
      });
  }

  return {
    steamId,
    username,
    isLoggedIn,
    isRegistering,
    login,
  }
});
