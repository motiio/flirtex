import cn from 'classnames';
import styles from './CustomButton.module.scss';
import { Loader } from '../Loader/Loader';

interface BaseButtonProps {
  text: string;
  onClick: () => void;
  isDisabled?: boolean;
  isLoading?: boolean;
}

export const CustomButton = ({ text, onClick, isDisabled, isLoading }: BaseButtonProps) => {
  const currentDisabledState = !!(isDisabled || isLoading);
  const clickHandler = () => {
    if (!currentDisabledState) {
      onClick();
    }
  };

  return (
    <div
      className={cn(styles.container, { [styles.disabled]: currentDisabledState, [styles.loading]: isLoading })}
      onClick={clickHandler}
      role="presentation"
    >
      {isLoading && <div className={styles.loaderWrapper} />}
      <div className={styles.textWrapper}>{text}</div>
      {isLoading && (
        <div className={styles.loaderWrapper}>
          <Loader size="XS" />
        </div>
      )}
    </div>
  );
};
