<script setup lang="ts">
import WatchListItem from '@/components/WatchListItem.vue'
import { apolloClient } from '@/plugins/apollo'
import { useQuery, provideApolloClient } from '@vue/apollo-composable'
import { GET_WATCHLIST } from '@/graphql/queries'
import { ref, watch } from 'vue'
import { useAuthToken } from '@/stores/authStore'
import { storeToRefs } from 'pinia'

const { authToken } = storeToRefs(useAuthToken())
const watchlist = ref<any[]>([])

const { result } = provideApolloClient(apolloClient)(() =>
  useQuery(
    GET_WATCHLIST,
    {},
    {
      fetchPolicy: 'network-only',
      context: {
        headers: {
          Authorization: `${authToken.value}`,
        },
      },
    },
  ),
)

watch(result, (data) => {
  if (data.getWatchlist) {
    watchlist.value = data.getWatchlist
  }
})
</script>
<template>
  <div class="flex flex-col items-center gap-y-6 pt-4">
    <h2 class="text-2xl font-bold text-gray-800 mb-4">Your Watchlist</h2>
    <div class="bg-white shadow-md rounded-lg p-4 max-h-96 overflow-y-auto border border-gray-300">
      <ul v-if="watchlist && watchlist.length" class="space-y-4">
        <WatchListItem v-for="item in watchlist" :key="item.id" :item="item" />
      </ul>
      <p v-else class="text-center text-gray-500">
        Your watchlist is empty. Start adding some anime!
      </p>
    </div>
  </div>
</template>
