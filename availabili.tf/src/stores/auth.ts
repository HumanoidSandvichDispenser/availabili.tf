import { defineStore } from "pinia";
import { ref } from "vue";
import { useClientStore } from "./client";
import { useRouter, type LocationQuery } from "vue-router";
import { type GetUserResponse, type PlayerSchema } from "@/client";

export const useAuthStore = defineStore("auth", () => {
  const clientStore = useClientStore();
  const client = clientStore.client;

  const user = ref<GetUserResponse | null>(null);
  const steamId = ref("");
  const username = ref("");
  const isLoggedIn = ref(false);
  const isRegistering = ref(false);
  const hasCheckedAuth = ref(false);
  const isAdmin = ref(false);
  const realUser = ref<PlayerSchema | null>(null);
  const discordId = ref<string | null>("");

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
        isAdmin.value = response.isAdmin || (response.realUser?.isAdmin ?? false);
        realUser.value = response.realUser ?? null;
        discordId.value = response.discordId ?? "";

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

  async function getAllUsers() {
    return client.default.getAllUsers();
  }

  async function setDoas(doasSteamId: string) {
    return client.default.setDoas(doasSteamId)
      .then((response) => {
        if (user.value) {
          realUser.value = {
            steamId: user.value.steamId,
            username: user.value.username,
            isAdmin: user.value.isAdmin,
          };
        }
        steamId.value = response.steamId;
        username.value = response.username;
      });
  }

  async function unsetDoas() {
    return client.default.unsetDoas()
      .then((_) => {
        if (realUser.value) {
          steamId.value = realUser.value.steamId;
          username.value = realUser.value.username;
        }
        realUser.value = null;
      });
  }

  return {
    steamId,
    username,
    isAdmin,
    realUser,
    discordId,
    isLoggedIn,
    hasCheckedAuth,
    isRegistering,
    getUser,
    getAllUsers,
    setDoas,
    unsetDoas,
    login,
    logout,
    setUsername,
  }
});
