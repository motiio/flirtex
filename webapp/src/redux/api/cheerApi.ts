import { api } from './cheerService';
import {
  AuthRequestI,
  DeckResponseI,
  FilterI,
  InterestsResponseI,
  LikeReactionsResponseI,
  PhotoI,
  ProfileInterestsI,
  ProfileRequestI,
  ProfileResponseI,
  ProfileUpdateRequestI,
  RefreshTokenI,
  TokensI,
} from '../../utils/interfaces';
import { PaginationRequestI } from '../../utils/interfaces/request/pagination';
import { MatchesResponseI } from '../../utils/interfaces/response/matches';

const injectedRtkApi = api.injectEndpoints({
  endpoints: (build) => ({
    refreshTokensAuthPut: build.mutation<TokensI, RefreshTokenI>({
      query: (queryArg) => ({
        url: '/auth',
        method: 'PUT',
        headers: { 'user-agent': queryArg.userAgent },
        params: { refresh_token: queryArg.refreshToken },
      }),
    }),
    loginUserAuthPost: build.mutation<TokensI, AuthRequestI>({
      query: (queryArg) => ({
        url: '/auth',
        method: 'POST',
        body: queryArg.userLoginRequest,
        headers: { 'user-agent': queryArg.userAgent },
      }),
    }),
    getMyProfileProfileGet: build.query<ProfileResponseI, void>({
      query: () => ({
        url: '/profile',
      }),
      extraOptions: { maxRetries: 0 },
      providesTags: ['Profile'],
    }),
    deleteMyProfile: build.query<null, void>({
      query: () => ({ url: '/profile', method: 'DELETE' }),
    }),
    registerProfileProfilePost: build.mutation<ProfileResponseI, ProfileRequestI>({
      query: (queryArg) => ({ url: '/profile', method: 'POST', body: queryArg }),
    }),
    updateProfilePatch: build.mutation<ProfileResponseI, ProfileUpdateRequestI>({
      query: (profileInfo) => ({ url: '/profile', method: 'PATCH', body: profileInfo }),
      invalidatesTags: ['Profile'],
    }),
    addInterestsToProfilePost: build.mutation<InterestsResponseI, ProfileInterestsI>({
      query: (queryArg) => ({ url: '/profile/interests', method: 'PUT', body: queryArg }),
    }),
    getInterestsGet: build.query<InterestsResponseI, void>({
      query: () => ({ url: '/interests' }),
    }),
    uploadProfilePhotoPost: build.mutation<PhotoI, FormData>({
      query: (photoList) => ({
        url: '/profile/photo',
        method: 'POST',
        body: photoList,
      }),
    }),
    removePhotoFromProfileDelete: build.mutation<null, string>({
      query: (id) => ({
        url: `/profile/photo/${id}`,
        method: 'DELETE',
      }),
    }),
    editPhotoOrderInProfilePatch: build.mutation<null, { photo_id: string; displaying_order: number }[]>({
      query: (photoInfo) => ({
        url: '/profile/photo',
        method: 'PATCH',
        body: { new_order: photoInfo },
      }),
    }),
    getPhotoByUrlGet: build.query<Blob, string>({
      query: (url) => ({
        url: `https://cdn.lovolab.ru/${url}`,
        responseHandler: async (response) => response.blob(),
        validateStatus: (response) => response.status === 200 && response.ok,
        cache: 'no-cache',
      }),
    }),
    getDeckPost: build.query<DeckResponseI, void>({
      query: () => ({
        url: '/deck/',
        method: 'POST',
      }),
    }),
    setLikePost: build.mutation<null, string>({
      query: (profileId) => ({
        url: `/deck/like/${profileId}`,
        method: 'POST',
      }),
    }),
    skipPost: build.mutation<null, string>({
      query: (profileId) => ({
        url: `/deck/skip/${profileId}`,
        method: 'POST',
      }),
    }),
    getFilterGet: build.query<FilterI, void>({
      query: () => ({
        url: '/deck/filter',
        method: 'GET',
      }),
      providesTags: ['Filter'],
    }),
    updateFilterPatch: build.mutation<FilterI, FilterI>({
      query: (filterData) => ({
        url: '/deck/filter',
        method: 'PATCH',
        body: filterData,
      }),
      invalidatesTags: ['Filter'],
    }),
    getLikeReactionGet: build.query<LikeReactionsResponseI, PaginationRequestI>({
      query: ({ page, limit = 10 }) => ({
        url: `/deck/like_reactions?limit=${limit}&offset=${page * limit}`,
      }),
      serializeQueryArgs: ({ endpointName }) => {
        return endpointName;
      },
      forceRefetch({ currentArg, previousArg }) {
        if (currentArg && currentArg.page !== 0 && previousArg?.page === undefined) {
          currentArg.page = 0;
        }

        return currentArg?.page !== previousArg?.page;
      },
    }),
    getMatchesGet: build.query<MatchesResponseI, PaginationRequestI>({
      query: ({ page, limit = 10 }) => ({
        url: `/deck/matches?limit=${limit}&offset=${page * limit}`,
      }),
      serializeQueryArgs: ({ endpointName }) => {
        return endpointName;
      },
      merge: (currentCache, newItems, { arg: { page } }) => {
        if (page === 0) {
          currentCache.profiles = newItems.profiles;
        } else {
          currentCache.profiles.push(...newItems.profiles);
        }
        currentCache.pagination = newItems.pagination;
      },
      // Refetch when the page arg changes
      forceRefetch({ currentArg, previousArg }) {
        if (currentArg && currentArg.page !== 0 && previousArg?.page === undefined) {
          currentArg.page = 0;
        }

        return currentArg?.page !== previousArg?.page;
      },
    }),
    getProfileByIdGet: build.query<ProfileResponseI, string>({
      query: (profileId) => `/profile/${profileId}`,
    }),
  }),
  overrideExisting: false,
});

export { injectedRtkApi as cheerApi };

export const {
  useLoginUserAuthPostMutation,
  useRegisterProfileProfilePostMutation,
  useGetMyProfileProfileGetQuery,
  useLazyGetMyProfileProfileGetQuery,
  useGetInterestsGetQuery,
  useLazyDeleteMyProfileQuery,
  useUploadProfilePhotoPostMutation,
  useGetLikeReactionGetQuery,
  useUpdateProfilePatchMutation,
  useRemovePhotoFromProfileDeleteMutation,
  useEditPhotoOrderInProfilePatchMutation,
  useGetDeckPostQuery,
  useSetLikePostMutation,
  useSkipPostMutation,
  useGetFilterGetQuery,
  useUpdateFilterPatchMutation,
  useGetProfileByIdGetQuery,
  useGetMatchesGetQuery,
} = injectedRtkApi;
