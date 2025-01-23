import gql from 'graphql-tag'

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
