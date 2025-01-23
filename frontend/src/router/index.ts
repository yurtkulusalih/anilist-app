import { createRouter, createWebHistory } from 'vue-router'
import { useAuthToken } from '@/stores/authStore'
import HomeView from '@/views/HomeView.vue'
import { storeToRefs } from 'pinia'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/search',
      name: 'search',
      component: () => import('@/views/SearchView.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/RegisterView.vue'),
    },
  ],
})

router.beforeEach((to, _from, next) => {
  const { authToken } = storeToRefs(useAuthToken())
  if ((to.name === 'login' || to.name === 'register') && authToken.value) {
    next({ name: 'home' })
  } else {
    next()
  }
})

export default router
