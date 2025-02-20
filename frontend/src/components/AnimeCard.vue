<script setup lang="ts">
import { useAuthToken } from '@/stores/authStore'
import { ADD_TO_WATCHLIST, useMutationWithProvider } from '@/graphql'
import { storeToRefs } from 'pinia'
import { ref } from 'vue'

const authTokenStore = useAuthToken()

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
    inWatchlist: boolean
  }
}

const props = defineProps<IProps>()

const itemInWatchlist = ref<boolean>(props.anime.inWatchlist)

const { mutate: addToWatchlist, onDone, onError } = useMutationWithProvider(ADD_TO_WATCHLIST)

const onClickAddToWatchlist = (id: number) => {
  addToWatchlist(
    { animeId: id },
    {
      context: {
        headers: {
          Authorization: `${authTokenStore?.authToken}`,
        },
      },
    },
  )

  onDone((result) => {
    if (result.data?.addToWatchlist) itemInWatchlist.value = true
  })

  onError((error) => {
    console.error(error)
    alert('An error occurred. Please try again.')
  })
}
</script>
<template>
  <div class="flex flex-col justify-between bg-white shadow-md rounded-lg overflow-hidden">
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
    <div v-if="authTokenStore.isUserLoggedIn" class="mt-auto p-4 border-t">
      <button
        data-test="anime-card-add-to-watchlist-btn"
        class="text-white px-4 py-2 rounded-md w-full"
        :class="
          itemInWatchlist
            ? 'bg-gray-500 cursor-not-allowed hover:'
            : 'bg-blue-500 hover:bg-blue-600 transition-colors'
        "
        @click="() => onClickAddToWatchlist(anime.id)"
      >
        {{ itemInWatchlist ? 'Added' : 'Add to Watchlist' }}
      </button>
    </div>
  </div>
</template>
