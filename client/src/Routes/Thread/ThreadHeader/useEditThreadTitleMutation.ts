import { useMutation } from "@apollo/react-hooks"
import gql from "graphql-tag"
import { IMutationError } from "../../../types"
import { IThread } from "../Thread.types"

const EDIT_THREAD_TITLE = gql`
  mutation EditThreadTitle($input: EditThreadTitleInput!) {
    editThreadTitle(input: $input) {
      errors {
        message
        location
        type
      }
      thread {
        id
        title
      }
    }
  }
`

interface IEditThreadTitleMutationData {
  editThreadTitle: {
    errors: Array<IMutationError> | null
    thread: {
      id: string
      title: string
    } | null
  }
}

interface IEditThreadTitleMutationVariables {
  input: {
    thread: string
    title: string
  }
}

const useEditThreadTitleMutation = (thread: IThread) => {
  const [mutation, { data, error, loading }] = useMutation<
    IEditThreadTitleMutationData,
    IEditThreadTitleMutationVariables
  >(EDIT_THREAD_TITLE)

  return {
    data,
    error,
    loading,
    editThreadTitle: (title: string) => {
      return mutation({
        variables: {
          input: { title, thread: thread.id },
        },
      })
    },
  }
}

export default useEditThreadTitleMutation