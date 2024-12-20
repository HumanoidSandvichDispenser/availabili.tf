import { defineStore } from "pinia";
import { ref } from "vue";
import { useClientStore } from "./client";
import { useRouter, type LocationQuery } from "vue-router";
import { type PlayerSchema } from "@/client";

export const useAuthStore = defineStore("auth", () => {
  const clientStore = useClientStore();
  const client = clientStore.client;

  const user = ref<PlayerSchema | null>(null);
  const steamId = ref("");
  const username = ref("");
  const isLoggedIn = ref(false);
  const isRegistering = ref(false);
  const hasCheckedAuth = ref(false);

  const router = useRouter();

  async function getUser() {
    if (hasCheckedAuth.value) {
      if (!isLoggedIn.value) {
        throw new Error("Not logged in");
      }

      return user.value;
    }

    return clientStore.call(
      getUser.name,
      () => client.default.getUser(),
      (response) => {
        hasCheckedAuth.value = true;
        isLoggedIn.value = true;
        steamId.value = response.steamId;
        username.value = response.username;
        user.value = response;
        return response;
      },
      undefined,
      () => hasCheckedAuth.value = true,
    );
  }

  async function login(queryParams: LocationQuery) {
    // TODO: replace with client call once it's implemented
    return fetch("/api/login/authenticate", {
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

  async function logout() {
    return client.default.deleteApiLogin()
      .then(() => router.push("/"));
  }

  async function setUsername(name: string) {
    return client.default.setUsername({ username: name })
      .then((response) => {
        username.value = response.username;
      });
  }

  return {
    steamId,
    username,
    isLoggedIn,
    hasCheckedAuth,
    isRegistering,
    getUser,
    login,
    logout,
    setUsername,
  }
});
