import { flushPromises, mount } from '@vue/test-utils'
import { beforeEach, describe, expect, vi, test, beforeAll, afterEach, afterAll } from 'vitest'
import AnimeCard from '@/components/AnimeCard.vue'
import { useAuthToken } from '@/stores/authStore'
import { createTestingPinia } from '@pinia/testing'
import { ADD_TO_WATCHLIST } from '@/graphql'
import { setupServer } from 'msw/node'
import { graphql, HttpResponse } from 'msw'

const server = setupServer(
  graphql.mutation(ADD_TO_WATCHLIST, () => {
    return HttpResponse.json({ data: { addToWatchlist: true } })
  }),
)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

const anime = {
  id: 1,
  title: 'Test Anime',
  coverImage: 'test-image.jpg',
  description: 'Test description',
  averageScore: 80,
  startDate: '2021-01-01',
  endDate: '2021-12-31',
  status: 'FINISHED',
  inWatchlist: false,
}

describe('/components/AnimeCard.vue', () => {
  let wrapper: any
  beforeEach(() => {
    wrapper = mount(AnimeCard, {
      props: { anime },
      global: { plugins: [createTestingPinia({ createSpy: vi.fn() })] },
    })

    const store = useAuthToken()
    store.authToken = 'test-token'
  })
  test('adds anime to watchlist when btn is clicked', async () => {
    const button = wrapper?.get('[data-test="anime-card-add-to-watchlist-btn"]')
    expect(button.text()).toBe('Add to Watchlist')

    button.trigger('click')
    await flushPromises()

    expect(wrapper.vm.itemInWatchlist).toBe(true)
    expect(button.text()).toBe('Added')
  })
})
