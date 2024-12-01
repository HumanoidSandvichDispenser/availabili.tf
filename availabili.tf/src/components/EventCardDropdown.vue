<script setup lang="ts">
import type { EventWithPlayerSchema } from '@/client';
import { RouterLink } from "vue-router";
import {
  DropdownMenuRoot,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuPortal,
} from "radix-vue";


defineProps<{
  event: EventWithPlayerSchema;
}>();

const emit = defineEmits<{
  deleteEvent: []
}>();
</script>

<template>
  <DropdownMenuRoot>
    <DropdownMenuTrigger className="icon">
      <i class="bi bi-three-dots" />
    </DropdownMenuTrigger>
    <DropdownMenuPortal>
      <DropdownMenuContent className="shadow">
        <DropdownMenuItem>
          <RouterLink class="button" :to="{
            name: 'roster-builder-event',
            params: { eventId: event.event.id }
          }">
            <button>
              <i class="bi bi-pencil margin" />
              Edit
            </button>
          </RouterLink>
        </DropdownMenuItem>
        <DropdownMenuItem>
          <button class="destructive" @click="emit('deleteEvent')">
            <i class="bi bi-trash margin" />
            Delete
          </button>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenuPortal>
  </DropdownMenuRoot>
</template>
