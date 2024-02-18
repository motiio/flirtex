import { Skeleton } from '../../../../UI';
import { generateId } from '../../../../utils/handlers/generateId';
import styles from './Card.module.scss';

export const CardSkeleton = () => {
  return <Skeleton key={generateId()} className={styles.cardWrapper} />;
};
