import styles from './AppLoad.module.scss';
import { Loader } from '../../UI';
import { ReactComponent as Icon } from '../../../public/logo.svg';

export const AppLoad = () => (
  <div className={styles.container}>
    <div />
    <div className={styles.icon}>
      <Icon />
    </div>
    <div className={styles.description}>
      <Loader size="S" />
    </div>
  </div>
);
