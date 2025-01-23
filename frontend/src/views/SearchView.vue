<script setup lang="ts">
import { ref, watch } from 'vue'
import { SEARCH_ANIME } from '@/graphql/queries'
import { apolloClient } from '@/plugins/apollo'
import { useQuery, provideApolloClient } from '@vue/apollo-composable'
import AnimeCard from '@/components/AnimeCard.vue'

const searchTerm = ref<string>('')
const results = ref<any[]>([])

const searchAnime = () => {
  const { result: animelist } = provideApolloClient(apolloClient)(() =>
    useQuery(SEARCH_ANIME, {
      search: searchTerm.value,
    }),
  )

  const unwatch = watch(animelist, (data) => {
    if (data.animelist) {
      results.value = data.animelist
      unwatch()
    }
  })
}
</script>

<template>
  <div class="flex flex-col items-center gap-y-6 pt-4">
    <div class="flex gap-x-4 justify-center w-full">
      <input v-model="searchTerm" placeholder="Search Anime" class="border p-2 w-[60%]" />
      <button class="bg-blue-500 text-white px-4 py-2" @click="searchAnime">Search</button>
    </div>
    <div v-if="results.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 w-[60%]">
      <AnimeCard v-for="anime in results" :key="anime.id" :anime="anime" />
    </div>
    <!-- Empty State -->
    <p v-else class="text-center text-gray-500">
      No results found. Try searching for something else.
    </p>
  </div>
</template>
