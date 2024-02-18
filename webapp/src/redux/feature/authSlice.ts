import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { cheerApi } from '../api/cheerApi';
import { TokensI } from '../../utils/interfaces';

interface AuthState {
  accessToken: string;
  refreshToken: string;
  hasProfile: boolean | null;
  profileId: string;
  settingIsVisible: boolean;
}

const initialState: AuthState = {
  accessToken: '',
  refreshToken: '',
  hasProfile: null,
  profileId: '000',
  settingIsVisible: false,
};

export const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    addTokens(state, { payload }: PayloadAction<TokensI>) {
      state.accessToken = payload.access_token;
      state.refreshToken = payload.refresh_token;
    },
    setHasProfile(state, { payload }: PayloadAction<boolean | null>) {
      state.hasProfile = payload;
    },
    addProfileId(state, { payload }: PayloadAction<string>) {
      state.profileId = payload;
    },
    setSettingIsVisible(state, { payload }: PayloadAction<boolean>) {
      state.settingIsVisible = payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addMatcher(cheerApi.endpoints.loginUserAuthPost.matchFulfilled, (state, { payload }) => {
        state.accessToken = payload.access_token;
        state.refreshToken = payload.refresh_token;
      })
      .addMatcher(cheerApi.endpoints.getMyProfileProfileGet.matchFulfilled, (state) => {
        state.hasProfile = true;
      })
      .addMatcher(cheerApi.endpoints.deleteMyProfile.matchFulfilled, (state) => {
        state.hasProfile = false;
      })
      .addMatcher(cheerApi.endpoints.getMyProfileProfileGet.matchRejected, (state, { payload }) => {
        if (payload?.status === 404) {
          state.hasProfile = false;
        }
      });
  },
});

export default authSlice.reducer;
