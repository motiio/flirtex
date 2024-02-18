import cn from 'classnames';
import styles from './ErrorComponent.module.scss';
import { ErrorT } from '../../utils/interfaces';
import { CustomButton, Snackbar } from '../../UI';

interface ErrorComponentProps {
  isWrongPage?: boolean;
  error?: ErrorT;
  onClick?: VoidFunction;
}

export const ErrorComponent = ({ isWrongPage, error, onClick }: ErrorComponentProps) => {
  const subTitle = onClick ? 'Попробовать еще раз' : 'Вернуться на главную страницу';

  const handleClickBack = () => {
    if (onClick) {
      onClick();
    } else {
      window.location.replace('/');
    }
  };

  return (
    <div className={cn(styles.container, { [styles.wrongPage]: isWrongPage })}>
      <div className={styles.title}>Что-то пошло не так...</div>
      <div className={styles.subTitle}>{subTitle}</div>
      <div className={styles.button}>
        <CustomButton text="ЖМЯК" onClick={handleClickBack} />
      </div>
      <Snackbar shouldRender={!!error} description={error} />
    </div>
  );
};
