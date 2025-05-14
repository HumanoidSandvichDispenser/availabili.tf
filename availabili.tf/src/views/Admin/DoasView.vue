<script setup lang="ts">
import { type PlayerSchema, type PlayerSchemaList } from "@/client";
import { useAuthStore } from "@/stores/auth";
import { onMounted, ref } from "vue";

//const cookies = useCookies(["doas"], { doNotParse: true, autoUpdateDependencies: true }, universalCookie);
const doas = ref<PlayerSchema | undefined>();
const users = ref<PlayerSchemaList>([]);
const authStore = useAuthStore();

onMounted(() => {
  authStore.getAllUsers()
    .then((response) => {
      users.value = response;
      //doas.value = response.find(user => user.steamId === cookies.get("doas"));
    });
});

function setDoas() {
  if (doas.value) {
    authStore.setDoas(doas.value.steamId);
  } else {
    authStore.unsetDoas();
  }
}

function removeDoas() {
  doas.value = undefined;
  authStore.unsetDoas();
}
</script>

<template>
  <h2>Become User</h2>
  <p>
    Do as/become a specific user.
  </p>
  <div>
    <div class="form-group margin">
      <h3>User</h3>
      <v-select
        v-model="doas"
        :options="users"
        label="username"
        placeholder="Select a user"
        :clearable="true"
        :searchable="true"
        :close-on-select="true"
        :show-search-input="true"
      />
    </div>
    <div class="form-group margin">
      <div class="action-buttons">
        <button class="destructive-on-hover" @click="removeDoas">
          <i class="bi bi-trash" />
        </button>
        <button class="accent" @click="setDoas">
          <i class="bi bi-check" />
          Become {{ doas?.username }}
        </button>
      </div>
    </div>
  </div>
</template>
