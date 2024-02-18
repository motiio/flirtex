import { ReactComponent as CloseIcon } from '../../../assets/icons/close.svg';
import { ReactComponent as HeartIcon } from '../../../assets/icons/heart-custom.svg';
import { SwipeState } from '../../../utils/constants';

export const stickyMenu = [
  {
    value: SwipeState.skip,
    Icon: CloseIcon,
  },
  {
    value: SwipeState.like,
    Icon: HeartIcon,
  },
];
