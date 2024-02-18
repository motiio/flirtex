import styles from './InteractionModule.module.scss';
import { Cards } from '../Cards/Cards';

export const InteractionModule = () => {
  return (
    <div className={styles.interactionModuleContainer}>
      <div className={styles.titleWrapper}>
        <div className={styles.title}>Подписчики</div>
      </div>
      <Cards />
    </div>
  );
};
