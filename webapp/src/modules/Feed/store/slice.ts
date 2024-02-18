import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { BatchI } from '../../../utils/interfaces';
import { SwipeState } from '../../../utils/constants';

interface StepperState {
  canForceUpdate: boolean;
  filterIsView: boolean;
  sidebarIsShown: boolean;
  imageIsDrag: boolean;
  numberOfCardsViewed: number;
  profilesBatch: BatchI[];
  lateSwipeState: SwipeState;
}

const initialState: StepperState = {
  canForceUpdate: false,
  filterIsView: false,
  sidebarIsShown: false,
  imageIsDrag: false,
  numberOfCardsViewed: 0,
  profilesBatch: [],
  lateSwipeState: SwipeState.nothing,
};

const feedSlice = createSlice({
  name: 'feedPage',
  initialState,
  reducers: {
    setCanForceUpdate(state, { payload }: PayloadAction<boolean>) {
      state.canForceUpdate = payload;
    },
    setSidebarIsShown(state, { payload }: PayloadAction<boolean>) {
      state.sidebarIsShown = payload;
    },
    setFilterIsView(state, { payload }: PayloadAction<boolean>) {
      state.filterIsView = payload;
    },
    setImageIsDrag(state, { payload }: PayloadAction<boolean>) {
      state.imageIsDrag = payload;
    },
    addNumberOfCard(state) {
      state.numberOfCardsViewed += 1;
    },
    resetNumberOfCard(state) {
      state.numberOfCardsViewed = 0;
    },
    setNewProfilesBatch(state, { payload }: PayloadAction<BatchI[]>) {
      state.profilesBatch = payload;
    },
    addProfilesBatch(state, { payload }: PayloadAction<BatchI[]>) {
      state.profilesBatch = [...state.profilesBatch, ...payload];
    },
    removeFirstProfile(state) {
      state.profilesBatch = [...state.profilesBatch.slice(1)];
    },
    setLateSwipeState(state, { payload }: PayloadAction<SwipeState>) {
      state.lateSwipeState = payload;
    },
    reset(state) {
      state.canForceUpdate = false;
      state.filterIsView = false;
      state.sidebarIsShown = false;
      state.imageIsDrag = false;
    },
  },
});

export { feedSlice };
