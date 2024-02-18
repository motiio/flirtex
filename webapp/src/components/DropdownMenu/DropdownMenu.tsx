import cn from 'classnames';
import { MouseEvent } from 'react';
import styles from './DropdownMenu.module.scss';
import { DropdownConfigT } from '../../utils/interfaces/dropdown';

interface DropdownMenuProps {
  config: DropdownConfigT;
}

export const DropdownMenu = ({ config }: DropdownMenuProps) => {
  const clickItemHandler = (e: MouseEvent<HTMLDivElement>, isDisabled: boolean, onClick: VoidFunction) => {
    if (isDisabled) {
      e.stopPropagation();
    } else {
      onClick();
    }
  };

  return (
    <div className={styles.dropdownMenuContainer}>
      {config.map(({ text, Icon, onClick, type = 'default', isDisabled = false }) => (
        <div
          key={text}
          className={cn(styles.itemWrapper, styles[type], { [styles.disable]: isDisabled })}
          onClick={(e) => clickItemHandler(e, isDisabled, onClick)}
          role="presentation"
        >
          <div className={styles.icon}>
            <Icon />
          </div>
          <div className={styles.text}>{text}</div>
        </div>
      ))}
    </div>
  );
};
