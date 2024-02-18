import styles from './ChatLine.module.scss';
import { Skeleton } from '../../../../UI';

export const ChatLineSkeleton = () => {
  return (
    <div className={styles.chatLine}>
      <div className={styles.imageWrapper}>
        <Skeleton width={58} height={58} borderRadius="58px" />
      </div>
      <div className={styles.information}>
        <div className={styles.nameWrapper}>
          <Skeleton height={19} width={100} className={styles.name} />
          <Skeleton height={16} width={160} className={styles.description} />
        </div>
        <div className={styles.options}>
          <Skeleton height={24} width={24} />
        </div>
      </div>
    </div>
  );
};
