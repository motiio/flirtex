import { BaseQueryFn, FetchArgs, fetchBaseQuery, FetchBaseQueryError, retry } from '@reduxjs/toolkit/query/react';
import type { RootState } from '../store';
import { authSlice } from '../feature/authSlice';
import { TokensI } from '../../utils/interfaces';
import { MAX_TIMEOUT_TIME } from '../../utils/constants';

const baseQuery = fetchBaseQuery({
  baseUrl: 'https://lovolab.ru/api/v1',
  timeout: MAX_TIMEOUT_TIME,
  prepareHeaders: (headers, { getState }) => {
    // By default, if we have a token in the store, let's use that for authenticated requests
    const { accessToken } = (getState() as RootState).authReducer;

    if (accessToken) {
      headers.set('authorization', `Bearer ${accessToken}`);
    }

    return headers;
  },
});

const baseQueryWithReauth: BaseQueryFn<string | FetchArgs, unknown, FetchBaseQueryError> = async (
  args,
  api,
  extraOptions,
) => {
  let result = await baseQuery(args, api, extraOptions);

  if (result.error && result.error.status === 401) {
    const { refreshToken } = (api.getState() as RootState).authReducer;
    const { addTokens, setHasProfile } = authSlice.actions;

    if (!refreshToken) {
      return result;
    }

    // try to get a new token
    const refreshResult = await baseQuery(
      {
        url: '/auth',
        method: 'PUT',
        headers: { 'user-agent': 'updateToken' },
        body: { refresh_token: refreshToken },
      },
      api,
      extraOptions,
    );

    if (refreshResult.data) {
      // store the new token
      api.dispatch(addTokens(refreshResult.data as TokensI));
      // retry the initial query
      result = await baseQuery(args, api, extraOptions);
    } else {
      api.dispatch(setHasProfile(null));
      api.dispatch(addTokens({ refresh_token: '', access_token: '' }));
    }
  }
  return result;
};

export const baseQueryWithRetry = retry(baseQueryWithReauth, { maxRetries: 1 });
