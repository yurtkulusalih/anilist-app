import { flushPromises, mount } from '@vue/test-utils'
import { beforeEach, describe, expect, vi, test, beforeAll, afterEach, afterAll } from 'vitest'
import AnimeCard from '@/components/AnimeCard.vue'
import { useAuthToken } from '@/stores/authStore'
import { createTestingPinia, type TestingPinia } from '@pinia/testing'
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
  let pinia: TestingPinia
  beforeEach(() => {
    pinia = createTestingPinia({ createSpy: vi.fn() })
  })
  test('adds anime to watchlist when btn is clicked', async () => {
    const store = useAuthToken()
    store.authToken = 'test-token'

    wrapper = mount(AnimeCard, {
      props: { anime },
      global: { plugins: [pinia] },
    })
    const button = wrapper?.get('[data-test="anime-card-add-to-watchlist-btn"]')
    expect(button.text()).toBe('Add to Watchlist')

    button.trigger('click')
    await flushPromises()

    expect(wrapper.vm.itemInWatchlist).toBe(true)
    expect(button.text()).toBe('Added')
  })

  test('btn is not rendered if not logged in', () => {
    wrapper = mount(AnimeCard, {
      props: { anime },
      global: { plugins: [pinia] },
    })

    expect(() => wrapper?.get('[data-test="anime-card-add-to-watchlist-btn"]')).toThrowError()
  })
})
