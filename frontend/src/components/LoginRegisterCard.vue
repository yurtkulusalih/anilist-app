<script setup lang="ts">
import { ref } from 'vue'
import { LOGIN, CREATE_USER, useMutationWithProvider } from '@/graphql'
import { useAuthToken } from '@/stores/authStore'
import { useRouter } from 'vue-router'

interface IProps {
  type: 'login' | 'register'
}

const props = defineProps<IProps>()

const router = useRouter()
const { setAuthToken } = useAuthToken()

// Form fields
const username = ref<string>('')
const password = ref<string>('')
const confirmPassword = ref<string>('')

const isLogin = ref<boolean>(props.type === 'login')

const {
  mutate: loginUser,
  onDone: onLoginUser,
  onError: onErrorLogin,
} = useMutationWithProvider(LOGIN)
const { mutate: createUser, onDone: onCreateUser } = useMutationWithProvider(CREATE_USER)

const toggleForm = () => router.push({ path: isLogin.value ? '/register' : '/login' })

// Form submission
const handleSubmit = async () => {
  if (!isLogin.value && password.value !== confirmPassword.value) {
    alert('Passwords do not match.')
    return
  }

  if (isLogin.value) {
    loginUser({ username: username.value, password: password.value })
    onLoginUser((result) => {
      setAuthToken(result.data?.login)
      router.push({ path: '/' })
    })

    onErrorLogin((error) => {
      alert(error.message)
    })
  } else {
    createUser({ username: username.value, password: password.value })
    onCreateUser((result) => {
      console.log(result.data?.createUser)
      if (result.data?.createUser) toggleForm() // Switch to login form
    })
  }
}
</script>

<template>
  <div class="bg-white shadow-md rounded-lg p-8 max-w-md w-full">
    <!-- Card Title -->
    <h2 class="text-2xl font-bold text-center text-gray-800 mb-6">
      {{ isLogin ? 'Login' : 'Register' }}
    </h2>

    <!-- Input Fields -->
    <form @submit.prevent="handleSubmit">
      <div class="mb-4">
        <label for="username" class="block text-sm font-medium text-gray-700 mb-1">
          Username
        </label>
        <input
          v-model="username"
          type="text"
          id="username"
          placeholder="Enter your username"
          class="border rounded-md w-full p-2 focus:ring-2 focus:ring-blue-500"
          required
        />
      </div>

      <div class="mb-4">
        <label for="password" class="block text-sm font-medium text-gray-700 mb-1">
          Password
        </label>
        <input
          v-model="password"
          type="password"
          id="password"
          placeholder="Enter your password"
          class="border rounded-md w-full p-2 focus:ring-2 focus:ring-blue-500"
          required
        />
      </div>

      <!-- Confirm Password for Registration -->
      <div v-if="!isLogin" class="mb-4">
        <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-1">
          Confirm Password
        </label>
        <input
          v-model="confirmPassword"
          type="password"
          id="confirmPassword"
          placeholder="Confirm your password"
          class="border rounded-md w-full p-2 focus:ring-2 focus:ring-blue-500"
          required
        />
      </div>

      <!-- Submit Button -->
      <button
        type="submit"
        class="bg-blue-500 text-white py-2 px-4 rounded-md w-full hover:bg-blue-600 transition-colors"
      >
        {{ isLogin ? 'Login' : 'Register' }}
      </button>
    </form>

    <!-- Toggle Login/Register -->
    <p class="text-sm text-center text-gray-600 mt-4">
      {{ isLogin ? "Don't have an account?" : 'Already have an account?' }}
      <span class="text-blue-500 font-semibold cursor-pointer hover:underline" @click="toggleForm">
        {{ isLogin ? 'Register' : 'Login' }}
      </span>
    </p>
  </div>
</template>
