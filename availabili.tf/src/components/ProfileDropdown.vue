<script setup lang="ts">
import { useAuthStore } from "@/stores/auth";
import {
  DropdownMenuRoot,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuPortal,
} from "radix-vue";
import { RouterLink } from "vue-router";

const authStore = useAuthStore();

function logout() {
  authStore.logout();
}
</script>

<template>
  <DropdownMenuRoot>
    <DropdownMenuTrigger className="profile-button">
      {{ authStore.username }}
      <i class="bi bi-chevron-down" />
    </DropdownMenuTrigger>
    <DropdownMenuPortal>
      <DropdownMenuContent className="shadow">
        <DropdownMenuItem>
          <RouterLink class="button" :to="{ 'name': 'user-settings' }">
            <button>
              <i class="bi bi-gear margin" />
              Settings
            </button>
          </RouterLink>
        </DropdownMenuItem>
        <DropdownMenuItem>
          <RouterLink class="button" to="/teams">
            <button>
              <i class="bi bi-people margin" />
              Teams
            </button>
          </RouterLink>
        </DropdownMenuItem>
        <DropdownMenuItem>
          <button class="destructive" @click="logout">
            <i class="bi bi-box-arrow-right margin" />
            Log out
          </button>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenuPortal>
  </DropdownMenuRoot>
</template>

<style scoped>
.profile-button {
  background-color: transparent;
  font-size: inherit;
}

.profile-button:hover {
  background-color: var(--surface-0);
}
</style>
