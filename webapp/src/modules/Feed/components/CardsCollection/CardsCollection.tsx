import { memo } from 'react';
import styles from './CardsCollection.module.scss';
import { BatchI } from '../../../../utils/interfaces';

interface CardsCollectionProps {
  profiles: BatchI[];
}

export const CardsCollection = memo(({ profiles }: CardsCollectionProps) => {
  return (
    <div className={styles.cardsCollectionContainer}>
      {profiles.map((profile, index) => (
        <div key={profile.photos[0].id} className={styles.card} style={{ zIndex: 10 - index }}>
          <img src={profile.photos[0].url} alt={profile.name} />
        </div>
      ))}
    </div>
  );
});
