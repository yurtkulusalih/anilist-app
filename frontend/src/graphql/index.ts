import gql from 'graphql-tag'
import { useMutation, provideApolloClient } from '@vue/apollo-composable'
import { apolloClient } from '@/plugins/apollo'

/**
 * Query
 */
export const SEARCH_ANIME = gql`
  query ($search: String!) {
    animelist(search: $search) {
      id
      title
      description
      coverImage
      averageScore
      status
      startDate
      endDate
    }
  }
`

export const GET_WATCHLIST = gql`
  query {
    getWatchlist {
      averageScore
      coverImage
      id
      title
      endDate
      startDate
      status
    }
  }
`
/**
 * Query
 */

/**
 * Mutation
 */
export const LOGIN = gql`
  mutation ($username: String!, $password: String!) {
    login(username: $username, password: $password)
  }
`

export const CREATE_USER = gql`
  mutation ($username: String!, $password: String!) {
    createUser(username: $username, password: $password)
  }
`

export const ADD_TO_WATCHLIST = gql`
  mutation ($animeId: Int!) {
    addToWatchlist(animeId: $animeId)
  }
`
/**
 * Mutation
 */

export const useMutationWithProvider = (query: any) => {
  return provideApolloClient(apolloClient)(() => useMutation(query))
}
