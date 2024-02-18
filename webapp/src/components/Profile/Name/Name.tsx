import cn from 'classnames';
import styles from './Name.module.scss';
import { ReactComponent as FemaleIcon } from '../../../assets/icons/woman.svg';
import { ReactComponent as MaleIcon } from '../../../assets/icons/man.svg';
import { ReactComponent as LocationIcon } from '../../../assets/icons/location.svg';
import { Gender } from '../../../utils/constants';

interface NameProps {
  name: string;
  age: number;
  gender: Gender;
  distance: number;
}

export const Name = ({ name, age, gender, distance }: NameProps) => {
  return (
    <div className={styles.nameContainer}>
      <div className={cn(styles.block, styles.customBlock)}>
        <div className={styles.nameWrapper}>
          <div className={cn(styles.title, styles.customTitle)}>
            {name}
            {', '}
            {age}
          </div>
          <div className={styles.genderWrapper}>{gender === Gender.male ? <MaleIcon /> : <FemaleIcon />}</div>
        </div>
        <div className={styles.distance}>
          <LocationIcon />
          &nbsp;&lt;&nbsp;
          {distance}
          &nbsp;км
        </div>
      </div>
    </div>
  );
};
