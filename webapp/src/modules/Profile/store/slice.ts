import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { InterestI } from '../../../utils/interfaces';
import { LocalPhotoI } from '../utils/interfaces';

interface ProfileStateI {
  removedPhotoIdList: string[];
  currentPhoto: LocalPhotoI | null;
  photoList: LocalPhotoI[];
  photoCanUpdate: boolean;
  interests: InterestI[];
  interestsCanUpdate: boolean;
  bio: string;
  bioCanUpdate: boolean;
}

const initialState: ProfileStateI = {
  removedPhotoIdList: [],
  currentPhoto: null,
  photoList: [],
  photoCanUpdate: false,
  interests: [],
  interestsCanUpdate: false,
  bio: '',
  bioCanUpdate: false,
};

const profilePageSlice = createSlice({
  name: 'profilePage',
  initialState,
  reducers: {
    addPhoto(state, { payload }: PayloadAction<LocalPhotoI>) {
      state.photoList = [...state.photoList, payload];
    },
    removePhoto(state, { payload }: PayloadAction<LocalPhotoI>) {
      const newPhotoList = [...state.photoList];
      newPhotoList.splice(payload.displaying_order - 1, 1);
      newPhotoList.forEach((photo, index) => {
        photo.displaying_order = index + 1;
        return photo;
      });
      state.currentPhoto = newPhotoList[0];
      state.photoList = [...newPhotoList];

      if (!payload.isLocal) {
        state.removedPhotoIdList = [...state.removedPhotoIdList, payload.id];
      }
    },
    setFirstPhoto(state, { payload: photoOrder }: PayloadAction<number>) {
      const newPhotoList = [...state.photoList];
      const movedPhoto = newPhotoList.splice(photoOrder - 1, 1)[0];
      newPhotoList.unshift(movedPhoto);
      newPhotoList.forEach((photo, index) => {
        photo.displaying_order = index + 1;
        return photo;
      });
      state.currentPhoto = newPhotoList[0];
      state.photoList = [...newPhotoList];
    },
    setCurrentPhoto(state, { payload }: PayloadAction<LocalPhotoI>) {
      state.currentPhoto = payload;
    },
    updateLocalPhoto(state, { payload }: PayloadAction<LocalPhotoI[]>) {
      state.photoList = state.photoList.map((photo) => {
        if (photo.isLocal) {
          const { id, url } = payload.shift() ?? photo;
          return { id, url, isLocal: false, displaying_order: photo.displaying_order };
        }
        return photo;
      });
    },
    setInterest(state, { payload }: PayloadAction<InterestI>) {
      if (state.interests.some((interest) => payload.id === interest.id)) {
        if (state.interests.length > 1) {
          state.interests = state.interests.filter((interest) => interest.id !== payload.id);
        }
      } else if (state.interests.length < 7) {
        state.interests = [...state.interests, payload];
      }
    },
    setBio(state, { payload }: PayloadAction<string>) {
      state.bio = payload;
    },
    reset(state) {
      state.bio = '';
      state.interests = [];
      state.photoList = [];
      state.currentPhoto = null;
    },
    setCanUpdateBio(state, { payload }: PayloadAction<boolean>) {
      state.bioCanUpdate = payload;
    },
    setCanUpdateInterests(state, { payload }: PayloadAction<boolean>) {
      state.interestsCanUpdate = payload;
    },
    setCanUpdatePhoto(state, { payload }: PayloadAction<boolean>) {
      state.photoCanUpdate = payload;
    },
  },
});

export { profilePageSlice };
