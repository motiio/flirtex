import cn from 'classnames';
import { ReactNode } from 'react';
import styles from './Button.module.scss';

interface ButtonProps {
  text: string;
  onClick: () => void;
  icon: ReactNode;
  type?: 'default' | 'lite' | 'disable' | 'accept' | 'outline';
  direction?: 'regular' | 'multiline';
  iconWrapper?: boolean;
  className?: string;
  isDisabled?: boolean;
  children?: ReactNode;
}

export const Button = ({
  text,
  icon,
  onClick,
  type = 'default',
  direction = 'regular',
  iconWrapper = false,
  className,
  isDisabled,
  children,
}: ButtonProps) => {
  const clickHandler = () => {
    if (!isDisabled) {
      onClick();
    }
  };

  return (
    <div
      className={cn(styles.container, styles[direction], styles[type], { [styles.disable]: isDisabled }, className)}
      onClick={clickHandler}
      role="presentation"
    >
      <div className={cn({ [styles.iconWrapper]: iconWrapper, [styles.iconWithoutWrapper]: !iconWrapper })}>{icon}</div>
      <div className={styles.textWrapper}>{text}</div>
      {children}
    </div>
  );
};
