<script setup lang="ts">
import { useInvitesStore } from "@/stores/teams/invites";
import { DialogClose, DialogContent, DialogDescription, DialogOverlay, DialogPortal, DialogRoot, DialogTitle, DialogTrigger } from "radix-vue";
import { ref } from "vue";
import { useRouter } from "vue-router";

const invitesStore = useInvitesStore();

const key = ref("");

const router = useRouter();

function submit() {
  invitesStore.consumeInvite(key.value)
    .then((response) => {
      console.log(response);
      router.push({
        name: "team-details",
        params: {
          id: response.teamId,
        }
      });
    });
}
</script>

<template>
  <DialogRoot>
    <DialogTrigger>
      <i class="bi bi-person-plus-fill margin" />
      Join a team
    </DialogTrigger>
    <DialogPortal>
      <DialogOverlay class="dialog-overlay" />
      <DialogContent>
        <DialogTitle>Join a team</DialogTitle>
        <DialogDescription>
          <p>
            Enter the invite key to join a team. Don't have an invite key? Ask
            your team leader to send you one.
          </p>
        </DialogDescription>
        <div class="form-group margin">
          <h3>Invite key</h3>
          <input type="text" placeholder="Invite key or URL" v-model="key" />
        </div>
        <div class="form-group">
          <div class="action-buttons">
            <DialogClose class="accent" aria-label="Close" @click="submit">
              <i class="bi bi-check" />
              Join
            </DialogClose>
          </div>
        </div>
      </DialogContent>
    </DialogPortal>
  </DialogRoot>
</template>

<style scoped>
[role="dialog"] {
  padding: 2rem;
  border-radius: 0.5rem;
}
</style>
