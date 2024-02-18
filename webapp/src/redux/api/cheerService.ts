import { RetryOptions } from '@reduxjs/toolkit/dist/query/retry';
import { BaseQueryFn, createApi, FetchArgs } from '@reduxjs/toolkit/query/react';
import { baseQueryWithRetry } from './baseQuery';
import { CustomErrorI } from '../../utils/interfaces';

export const api = createApi({
  /**
   * `reducerPath` is optional and will not be required by most users.
   * This is useful if you have multiple API definitions,
   * e.g. where each has a different domain, with no interaction between endpoints.
   * Otherwise, a single API definition should be used in order to support tag invalidation,
   * among other features
   */
  reducerPath: 'cheerApi',
  /**
   * A bare bones base query would just be `baseQuery: fetchBaseQuery({ baseUrl: '/' })`
   */
  baseQuery: baseQueryWithRetry as BaseQueryFn<string | FetchArgs, unknown, CustomErrorI, RetryOptions, {}>,
  /**
   * This api has endpoints injected in adjacent files,
   * which is why no endpoints are shown below.
   * If you want all endpoints defined in the same file, they could be included here instead
   */
  endpoints: () => ({}),
  tagTypes: ['Profile', 'Filter'],
});
