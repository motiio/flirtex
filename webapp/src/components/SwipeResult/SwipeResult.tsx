import cn from 'classnames';
import styles from './SwipeResult.module.scss';
import { ReactComponent as CloseIcon } from '../../assets/icons/close.svg';
import { ReactComponent as StarIcon } from '../../assets/icons/star.svg';
import { ReactComponent as HeartIcon } from '../../assets/icons/heart-custom.svg';
import { SwipeState } from '../../utils/constants';

interface SwipeResultProps {
  swipeState: SwipeState;
}

export const SwipeResult = ({ swipeState }: SwipeResultProps) => {
  if (swipeState === SwipeState.nothing) {
    return null;
  }

  return (
    <div className={cn(styles.swipeActionContainer, styles[swipeState])}>
      {swipeState === SwipeState.skip && <CloseIcon className={styles.skipIcon} />}
      {swipeState === SwipeState.save && <StarIcon />}
      {swipeState === SwipeState.like && <HeartIcon />}
    </div>
  );
};
