import { combineReducers, configureStore } from '@reduxjs/toolkit';
import { api } from './api/cheerService';
import authReducer from './feature/authSlice';
import { registrationSlice } from '../modules/Registration';
import { feedSlice } from '../modules/Feed';
import { profilePageSlice } from '../modules/Profile';
import { interactionSlice } from '../modules/Interaction';
import { matchesSlice } from '../modules/Matches';
import { appCoverSlice } from '../modules/AppCover';

const rootReducer = combineReducers({
  [api.reducerPath]: api.reducer,
  authReducer,
  registrationReducer: registrationSlice.reducer,
  feedReducer: feedSlice.reducer,
  profilePageReducer: profilePageSlice.reducer,
  interactionReducer: interactionSlice.reducer,
  matchesReducer: matchesSlice.reducer,
  appCoverReducer: appCoverSlice.reducer,
});

export const setupStore = () => {
  return configureStore({
    reducer: rootReducer,
    middleware: (getDefaultMiddleware) => {
      return getDefaultMiddleware({
        serializableCheck: false,
      }).concat(api.middleware);
    },
  });
};

export type RootState = ReturnType<typeof rootReducer>;
export type AppStore = ReturnType<typeof setupStore>;
export type AppDispatch = AppStore['dispatch'];
