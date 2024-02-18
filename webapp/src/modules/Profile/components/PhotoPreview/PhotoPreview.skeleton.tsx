import cn from 'classnames';
import styles from './PhotoPreview.module.scss';
import { Skeleton } from '../../../../UI';

export const PhotoPreviewSkeleton = () => {
  return (
    <Skeleton className={styles.photoPreviewContainer}>
      <div className={styles.bottomMenuWrapper}>
        <div className={styles.actionWrapper}>
          <Skeleton className={cn(styles.actionButton, styles.actionButtonSkeleton)} />
          <Skeleton className={cn(styles.actionButton, styles.actionButtonSkeleton)} />
          <Skeleton className={cn(styles.actionButton, styles.actionButtonSkeleton)} />
        </div>
      </div>
    </Skeleton>
  );
};
