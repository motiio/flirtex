import styles from './PhotoPreview.module.scss';
import { Skeleton } from '../../../UI';

export const PhotoPreviewSkeleton = () => {
  return <Skeleton className={styles.photoPreviewContainer} />;
};
