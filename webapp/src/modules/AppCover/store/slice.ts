import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { SettingItems } from '../utils/constants';

interface AppCoverState {
  settingItem: SettingItems;
  settingsIsShown: boolean;
  profileIsShown: boolean;
  profileId: string;
}

const initialState: AppCoverState = {
  settingItem: SettingItems.empty,
  settingsIsShown: false,
  profileIsShown: false,
  profileId: '',
};

const appCoverSlice = createSlice({
  name: 'appCover',
  initialState,
  reducers: {
    setSettingItem(state, { payload }: PayloadAction<SettingItems>) {
      state.settingItem = payload;
    },
    setSettingsIsShown(state, { payload }: PayloadAction<boolean>) {
      state.settingsIsShown = payload;
    },
    setProfileIsShown(state, { payload }: PayloadAction<boolean>) {
      state.profileIsShown = payload;
    },
    setProfileId(state, { payload }: PayloadAction<string>) {
      state.profileId = payload;
    },
    reset(state) {
      state.settingItem = SettingItems.empty;
      state.profileId = '';
      state.profileIsShown = false;
    },
  },
});

export { appCoverSlice };
