<script setup lang="ts">
import { useTeamDetails } from "@/composables/team-details";
import { useMatchesStore } from "@/stores/matches";
import { DialogClose, DialogContent, DialogDescription, DialogOverlay, DialogPortal, DialogRoot, DialogTitle, DialogTrigger } from "radix-vue";
import { ref } from "vue";

const matchesStore = useMatchesStore();

const { teamId } = useTeamDetails();

const urlsText = ref("");

function submit() {
  const ids = urlsText.value.split("\n")
    .map((url) => {
      const matchId = url.match(/logs\.tf\/(\d+)/);
      return matchId ? Number(matchId[1]) : NaN;
    })
    .filter((id) => !isNaN(id));

  matchesStore.submitMatches(ids, teamId.value)
    .then(() => {
      urlsText.value = "";
    });
}
</script>

<template>
  <DialogRoot>
    <DialogTrigger>
      <i class="bi bi-file-earmark-plus-fill margin" />
      Submit logs.tf matches
    </DialogTrigger>
    <DialogPortal>
      <DialogOverlay class="dialog-overlay" />
      <DialogContent>
        <DialogTitle>Submit logs.tf matches</DialogTitle>
        <DialogDescription>
          <p>
            Enter up to 10 logs.tf URLs (or match IDs) to submit them. This
            allows you to track your match stats and view them later.
          </p>
        </DialogDescription>
        <div class="form-group margin">
          <h3>logs.tf URLs</h3>
          <textarea
            v-model="urlsText"
            placeholder="Paste logs.tf URLs here (limit: 10)"
          />
        </div>
        <div class="form-group">
          <div class="action-buttons">
            <DialogClose class="accent" aria-label="Close" @click="submit">
              <i class="bi bi-check" />
              Submit
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
