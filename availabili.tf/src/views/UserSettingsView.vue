<script setup lang="ts">
import { useAuthStore } from "@/stores/auth";
import { computed, onMounted, ref } from "vue";

//const baseUrl = window.location.origin;

const redirectUri = computed(() => {
  return encodeURIComponent(window.location.origin + "/settings");
});

const oauthUrl = computed(() => {
  return "https://discord.com/oauth2/authorize" +
    "?client_id=1372254613692219392" +
    "&response_type=code" +
    `&redirect_uri=${redirectUri.value}` +
    "&scope=identify";
});

const displayName = ref("");

const authStore = useAuthStore();

function save() {
  authStore.setUsername(displayName.value);
}

onMounted(() => {
  displayName.value = authStore.username;
});
</script>

<template>
  <main>
    <div class="user-settings-container">
      <h1>User Settings</h1>
      <div class="form-group margin">
        <h3>
          Display Name
        </h3>
        <input v-model="displayName" />
      </div>
      <div class="form-group margin">
        <h3>
          Discord Account
        </h3>
        <!--p>
          Link your Discord account to your profile to enable Discord
          integration features. Contact
          <a href="https://discord.com/users/195789918474207233">@pyrofromcsgo</a>
          if you would like to manually link your account without logging in
          through Discord.
        </p-->
        <p v-if="authStore.discordId">
          Linked to Discord account <code>{{ authStore.discordId }}</code>.
        </p>
        <p v-else>
          Discord OAuth is not yet implemented.
          Contact <a href="https://discord.com/users/195789918474207233">@pyrofromcsgo</a>
          if you would like to link your Discord account.
        </p>
        <!--a :href="oauthUrl">
          <button>Link Discord Account</button>
        </a-->
      </div>
      <div class="form-group margin">
        <div class="action-buttons">
          <button class="accent" @click="save">Save</button>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
.user-settings-container {
  align-items: center;
  max-width: 500px;
  margin: auto;
}
</style>
