<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useAuthToken } from './stores/authStore'
import { RouterLink, RouterView, useRouter } from 'vue-router'

const { clearAuthToken } = useAuthToken()
const { isUserLoggedIn } = storeToRefs(useAuthToken())
const router = useRouter()
</script>

<template>
  <header>
    <nav class="flex justify-around items-center p-4 bg-blue-500 text-white">
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/search">Search</RouterLink>
      <RouterLink v-if="!isUserLoggedIn" to="/login">Login</RouterLink>
      <RouterLink v-if="!isUserLoggedIn" to="/register">Register</RouterLink>
      <RouterLink v-if="isUserLoggedIn" to="/watchlist">Watchlist</RouterLink>
      <span
        class="cursor-pointer"
        v-if="isUserLoggedIn"
        @click="
          () => {
            clearAuthToken()
            router.push('/login')
          }
        "
        >Logout</span
      >
    </nav>
  </header>
  <main class="bg-gray-100 min-h-screen">
    <RouterView />
  </main>
</template>
