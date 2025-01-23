<script setup lang="ts">
import { useAuthToken } from '@/stores/authStore'

const { isUserLoggedIn } = useAuthToken()

interface IProps {
  anime: {
    id: number
    title: string
    coverImage: string
    description: string
    averageScore: number
    startDate: string
    endDate: string
    status: string
  }
}

const props = defineProps<IProps>()
</script>
<template>
  <div class="flex flex-col justify-between bg-white shadow-md rounded-lg overflow-hidden">
    <!-- Card Image -->
    <img :src="props.anime.coverImage" alt="Anime Cover" class="h-48 w-full object-cover" />

    <!-- Card Content -->
    <div class="p-4">
      <h3 class="text-lg font-bold text-gray-800">{{ props.anime.title }}</h3>
      <p class="text-sm text-gray-600 mb-2 line-clamp-3" v-html="props.anime.description" />
      <p class="text-sm text-gray-800 font-semibold">
        Score: <span class="text-blue-500">{{ props.anime.averageScore }}</span>
      </p>
      <p class="text-sm text-gray-800">
        Aired: {{ props.anime.startDate }} -
        {{ (props.anime.endDate as string).includes('None') ? 'Ongoing' : props.anime.endDate }}
      </p>
      <p
        :class="{
          'text-green-500 font-semibold': props.anime.status === 'RELEASING',
          'text-gray-500': props.anime.status === 'FINISHED',
          'text-yellow-500': props.anime.status === 'NOT_YET_RELEASED',
        }"
        class="text-sm"
      >
        Status: {{ props.anime.status }}
      </p>
    </div>
    <div v-if="isUserLoggedIn" class="mt-auto p-4 border-t">
      <button
        class="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition-colors w-full"
        @click="() => console.log('In progress...')"
      >
        Add to Watchlist
      </button>
    </div>
  </div>
</template>
