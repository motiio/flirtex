import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { cheerApi } from '../../../redux/api/cheerApi';
import { LikeReactionsResponseI } from '../../../utils/interfaces';

interface InteractionState {
  profileId: string;
  isShownModal: boolean;
  page: number;
  likeReactions: LikeReactionsResponseI | null;
}

const initialState: InteractionState = {
  isShownModal: false,
  profileId: '',
  page: 0,
  likeReactions: null,
};

const interactionSlice = createSlice({
  name: 'interactionPage',
  initialState,
  reducers: {
    setProfileId(state, { payload }: PayloadAction<string>) {
      state.profileId = payload;
    },
    setIsShownModal(state, { payload }: PayloadAction<boolean>) {
      state.isShownModal = payload;
    },
    setPage(state, { payload }: PayloadAction<number>) {
      state.page = payload;
    },
    removeProfileFromLikeReactions(state, { payload: profileId }: PayloadAction<string>) {
      if (state.likeReactions) {
        state.likeReactions.profiles = state.likeReactions.profiles.filter((profile) => profile.id !== profileId);
      }
    },
    reset(state) {
      state.isShownModal = false;
      state.profileId = '';
    },
  },
  extraReducers: (builder) => {
    builder.addMatcher(cheerApi.endpoints.getLikeReactionGet.matchFulfilled, (state, { payload }) => {
      if (payload.pagination.offset === 0 && state.page !== 0) {
        state.likeReactions = payload;
        state.page = 0;
      } else if (payload.pagination.offset === 0 && state.page === 0) {
        state.likeReactions = payload;
      } else if (state.likeReactions !== null) {
        state.likeReactions = {
          pagination: payload.pagination,
          profiles: [...state.likeReactions.profiles, ...payload.profiles],
        };
      }
    });
  },
});

export { interactionSlice };
