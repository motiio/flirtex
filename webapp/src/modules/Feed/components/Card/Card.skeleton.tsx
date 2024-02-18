import cn from 'classnames';
import { Skeleton } from '../../../../UI';
import styles from './Card.module.scss';

export const CardSkeleton = () => {
  return (
    <div className={styles.cardContainer}>
      <Skeleton height="100svh" className={styles.imageWrapper} />
      <div className={styles.previewWrapper}>
        <div className={cn(styles.preview, styles.previewSkeleton)}>
          <Skeleton height={25} width="40%" className={styles.name} />
          <Skeleton height={25} width="30%" className={styles.distance} />
        </div>
        <div className={styles.barIcon}>
          <Skeleton height={22} width={28} className={styles.distance} />
        </div>
      </div>
      <div className={styles.filterWrapper}>
        <Skeleton className={styles.filterButton} />
      </div>
    </div>
  );
};
