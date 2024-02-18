import styles from './AboutProfile.module.scss';
import { Skeleton } from '../../../UI';

export const AboutProfileSkeleton = () => {
  return (
    <div className={styles.aboutProfileContainer}>
      <div className={styles.block}>
        <div className={styles.title}>Обо мне</div>
        <Skeleton className={styles.bioTextArea} />
      </div>
    </div>
  );
};
