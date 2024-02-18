import styles from './Cards.module.scss';
import { generateId } from '../../../../utils/handlers/generateId';
import { CardSkeleton } from '../Card/Card.skeleton';

export const CardsSkeleton = () => {
  return (
    <div className={styles.cardsContainer}>
      {Array.from(Array(9)).map(() => (
        <CardSkeleton key={generateId()} />
      ))}
    </div>
  );
};
