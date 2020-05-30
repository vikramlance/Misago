import React from "react"
import { Route, Switch } from "react-router-dom"
import { useSettingsContext } from "../../Context"
import { RouteErrorBoundary, RouteLoader, RouteNotFound } from "../../UI"
import * as urls from "../../urls"
import ThreadsAll from "./ThreadsAll"
import ThreadsCategory from "./ThreadsCategory"
import {
  ThreadsCategoriesModal,
  ThreadsCategoriesModalContextProvider,
} from "./ThreadsCategoriesModal"
import {
  ThreadsModerationModalContextProvider,
  ThreadsModerationModalDelete,
  ThreadsModerationModalMove,
} from "./ThreadsModeration"

const Threads: React.FC = () => {
  const settings = useSettingsContext()

  return (
    <ThreadsModerationModalContextProvider>
      <ThreadsModerationModalDelete />
      <ThreadsModerationModalMove />
      <ThreadsCategoriesModalContextProvider>
        <ThreadsCategoriesModal />
        <Switch>
          <Route
            path={urls.category({ id: ":id", slug: ":slug" })}
            render={() => (
              <RouteErrorBoundary>
                <ThreadsCategory />
              </RouteErrorBoundary>
            )}
            exact
          />
          <Route
            path={settings?.forumIndexThreads ? urls.index() : urls.threads()}
            render={() => (
              <RouteErrorBoundary>
                <ThreadsAll />
              </RouteErrorBoundary>
            )}
            exact
          />
          <Route
            path={urls.index()}
            render={() => (settings ? <RouteNotFound /> : <RouteLoader />)}
          />
        </Switch>
      </ThreadsCategoriesModalContextProvider>
    </ThreadsModerationModalContextProvider>
  )
}

export default Threads