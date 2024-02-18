import { ReactComponent as CloseIcon } from '../../../assets/icons/close.svg';
import { ReactComponent as HeartIcon } from '../../../assets/icons/heart-custom.svg';
import { Gender, SwipeState } from '../../../utils/constants';

export const filterOptions = [
  { name: Gender.male, text: 'Парней' },
  { name: Gender.female, text: 'Девушек' },
  { name: Gender.other, text: 'Всех' },
];

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
