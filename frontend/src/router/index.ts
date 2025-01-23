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
    {
      path: '/watchlist',
      name: 'watchlist',
      component: () => import('@/views/WatchlistView.vue'),
    },
  ],
})

router.beforeEach((to, _from, next) => {
  const { isUserLoggedIn } = storeToRefs(useAuthToken())
  if ((to.name === 'login' || to.name === 'register') && isUserLoggedIn.value) {
    next({ name: 'home' })
  } else if (to.name === 'watchlist' && !isUserLoggedIn.value) {
    next({ name: 'login' })
  } else {
    next()
  }
})

export default router
