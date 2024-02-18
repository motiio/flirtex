import cn from 'classnames';
import { ReactNode } from 'react';
import styles from './Chip.module.scss';

interface ChipProps {
  text: string;
  icon?: ReactNode;
  isSelected?: boolean;
  onClick?: () => void;
  className?: string;
}

export const Chip = ({ className, text, icon, isSelected = true, onClick }: ChipProps) => {
  const clickHandler = () => {
    if (onClick) {
      onClick();
    }
  };

  return (
    <div
      className={cn(styles.chip, { [styles.selected]: isSelected }, className)}
      onClick={clickHandler}
      role="presentation"
    >
      {icon && <div className={styles.icon}>{icon}</div>}
      {text}
    </div>
  );
};
