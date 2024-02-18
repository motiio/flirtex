import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface MatchesState {
  profileId: string;
  isShownModal: boolean;
  page: number;
}

const initialState: MatchesState = {
  isShownModal: false,
  profileId: '',
  page: 0,
};

const matchesSlice = createSlice({
  name: 'matches',
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
    reset(state) {
      state.isShownModal = false;
      state.profileId = '';
    },
  },
});

export { matchesSlice };
