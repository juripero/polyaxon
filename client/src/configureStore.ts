import {createStore, applyMiddleware} from "redux";
import "bootstrap/dist/css/bootstrap.min.css";
import * as _ from "lodash";

import thunkMiddleware from 'redux-thunk'
import { createLogger } from 'redux-logger'


import appReducer from "./reducers/app";
import {AppState} from "./constants/types";
import { loadState, saveState } from './localStorage'
import {getToken} from "./constants/utils";
import {receiveTokenActionCreator} from "./actions/token";

const configureStore = () => {
  const persistedState = loadState();
  const loggerMiddleware = createLogger();

  const store = createStore<AppState>(
    appReducer,
    // persistedState,
    applyMiddleware(
      thunkMiddleware,
      loggerMiddleware
    )
  );

  let token = getToken();
  if (token !== null) {
    store.dispatch(receiveTokenActionCreator(token.user, token));
  }

  store.subscribe(_.throttle(() => {
    saveState(store.getState())
  }, 1000));

  return store;
};

export default configureStore
