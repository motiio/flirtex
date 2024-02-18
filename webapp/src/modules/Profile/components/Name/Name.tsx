import cn from 'classnames';
import styles from './Name.module.scss';
import { Gender } from '../../../../utils/constants';
import { ReactComponent as FemaleIcon } from '../../../../assets/icons/woman.svg';
import { ReactComponent as MaleIcon } from '../../../../assets/icons/man.svg';

interface NameProps {
  name: string;
  age: number;
  gender: Gender;
}

export const Name = ({ name, age, gender }: NameProps) => {
  return (
    <div className={styles.nameContainer}>
      <div className={cn(styles.block, styles.customBlock)}>
        <div className={cn(styles.title, styles.customTitle)}>
          {name}
          {', '}
          {age}
        </div>
        <div className={styles.genderWrapper}>{gender === Gender.male ? <MaleIcon /> : <FemaleIcon />}</div>
      </div>
    </div>
  );
};
