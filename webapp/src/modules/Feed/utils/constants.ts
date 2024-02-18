import { MAX_WINDOW_WIDTH } from '../../../utils/constants';

export const SWIPE_ROW_THRESHOLD =
  window.innerWidth > MAX_WINDOW_WIDTH ? MAX_WINDOW_WIDTH * 0.3 : window.innerWidth * 0.3;
export const SWIPE_SIDEBAR_THRESHOLD = window.innerHeight * 0.2;
export const MIN_PROFILE_NUMBERS = 2;

export enum Animation {
  open = 'open',
  close = 'close',
  none = 'none',
}
