import cn from 'classnames';
import styles from './Filter.module.scss';
import { Skeleton } from '../../../../UI';

export const FilterSkeleton = () => {
  return (
    <div className={styles.filterContainer}>
      <Skeleton width={100} height={20} className={styles.label} />
      <div className={styles.block}>
        <Skeleton width={100} height={20} className={styles.blockTitle} />
        <div className={styles.sliderWrapper}>
          <Skeleton height={30} />
          <Skeleton height={30} />
          <Skeleton height={30} />
        </div>
      </div>
      <div className={styles.block}>
        <Skeleton width={100} height={20} className={styles.blockTitle} />
        <div className={styles.sliderWrapper}>
          <Skeleton height={15} />
          <Skeleton height={15} className={styles.title} />
        </div>
      </div>
      <div className={styles.block}>
        <Skeleton width={100} height={20} className={styles.blockTitle} />
        <div className={styles.sliderWrapper}>
          <Skeleton height={15} />
          <Skeleton height={15} className={styles.title} />
        </div>
      </div>
      <div className={cn(styles.block, styles.geo)}>
        <Skeleton height={40} className={styles.buttonWrapper} />
      </div>
    </div>
  );
};
