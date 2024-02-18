import { useNavigate } from 'react-router-dom';
import styles from './EmptyCard.module.scss';
import { CustomButton } from '../../../../UI';
import { PagesLink } from '../../../../utils/constants';

export const EmptyCard = () => {
  const navigate = useNavigate();

  const clickHandler = () => {
    navigate(PagesLink.feed);
  };

  return (
    <div className={styles.emptyCardContainer}>
      <div className={styles.title}>Тут пока пусто...</div>
      <CustomButton onClick={clickHandler} text="Познакомиться!" />
    </div>
  );
};
