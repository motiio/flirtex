import styles from './Interests.module.scss';
import { Skeleton } from '../../../../UI';
import { generateId } from '../../../../utils/handlers/generateId';

export const InterestsSkeleton = () => {
  return (
    <div className={styles.interestsContainer}>
      <div className={styles.block}>
        <div className={styles.title}>Интересы</div>
        <div className={styles.chipsWrapper}>
          {Array.from(Array(10)).map(() => (
            <Skeleton
              key={generateId()}
              height={34}
              width={Math.floor(Math.random() * (200 - 80 + 1)) + 80}
              className={styles.skeletonChips}
            />
          ))}
        </div>
      </div>
    </div>
  );
};
