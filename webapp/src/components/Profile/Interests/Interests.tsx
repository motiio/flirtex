import styles from './Interests.module.scss';
import { InterestIcon } from '../../InterestIcon/InterestIcon';
import { InterestI } from '../../../utils/interfaces';
import { Chip } from '../../../UI';

interface InterestsProps {
  interests: InterestI[];
}

export const Interests = ({ interests }: InterestsProps) => {
  return (
    <div className={styles.interestsContainer}>
      <div className={styles.block}>
        <div className={styles.title}>Интересы</div>
        <div className={styles.chipsWrapper}>
          {interests.map((interest) => (
            <Chip key={interest.id} text={interest.name} isSelected icon={<InterestIcon iconId={interest.id} />} />
          ))}
        </div>
      </div>
    </div>
  );
};
