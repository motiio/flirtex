import WebApp from '@twa-dev/sdk';
import { BackButton as BackButtonTg } from '@twa-dev/sdk/react';
import styles from './BackButton.module.scss';
import { ReactComponent as ArrowLeftIcon } from '../../assets/icons/arrow-left.svg';

interface BackButtonProps {
  onClose: VoidFunction;
}

export const BackButton = ({ onClose }: BackButtonProps) => {
  return WebApp.platform === 'unknown' ? (
    <div className={styles.topBarActions}>
      <div className={styles.icon} onClick={onClose} role="presentation">
        <ArrowLeftIcon />
      </div>
    </div>
  ) : (
    <BackButtonTg onClick={onClose} />
  );
};
