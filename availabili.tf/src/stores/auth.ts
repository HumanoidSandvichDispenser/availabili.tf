import { defineStore } from "pinia";
import { ref } from "vue";
import { useClientStore } from "./client";

export const useAuthStore = defineStore("auth", () => {
  const clientStore = useClientStore();
  const client = clientStore.client;

  const steamId = ref("");
  const username = ref("");
  const isLoggedIn = ref(false);
  const isRegistering = ref(false);
  const hasCheckedAuth = ref(false);

  async function getUser() {
    hasCheckedAuth.value = true;
    return clientStore.call(
      getUser.name,
      () => client.default.getUser(),
      (response) => {
        steamId.value = response.steamId;
        username.value = username.value;
        return response;
      }
    );
  }

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

  async function setUsername(username: string) {
    return client.default.setUsername({ username });
  }

  return {
    steamId,
    username,
    isLoggedIn,
    hasCheckedAuth,
    isRegistering,
    getUser,
    login,
    setUsername,
  }
});
