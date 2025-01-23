import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthToken = defineStore('authStore', () => {
  const authToken = ref<string | null>(localStorage.getItem('token'))

  const isUserLoggedIn = computed(() => authToken.value !== null)

  const setAuthToken = (token: string) => {
    authToken.value = token
    localStorage.setItem('token', token) // Persist token in localStorage
  }

  const clearAuthToken = () => {
    authToken.value = null
    localStorage.removeItem('token')
  }

  return {
    authToken,
    isUserLoggedIn,
    setAuthToken,
    clearAuthToken,
  }
})
