import styles from './Name.module.scss';
import { Skeleton } from '../../../../UI';

export const NameSkeleton = () => {
  return (
    <div className={styles.nameContainer}>
      <div className={styles.block}>
        <Skeleton width="50%" height={20} />
      </div>
    </div>
  );
};
