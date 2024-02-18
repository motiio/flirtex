import { ReactNode, useEffect, useState } from 'react';
import cn from 'classnames';
import styles from './Sidebar.module.scss';
import { BackButton } from '../BackButton/BackButton';

interface SidebarProps {
  isOpen: boolean;
  onOutsideClick: VoidFunction;
  children: ReactNode;
}

export const Sidebar = ({ isOpen, onOutsideClick, children }: SidebarProps) => {
  const [internalIsOpen, setInternalIsOpen] = useState(false);
  const [canCloseSidebar, setCanCloseSidebar] = useState(false);

  useEffect(() => {
    if (!isOpen && internalIsOpen) {
      setCanCloseSidebar(true);
    } else {
      setInternalIsOpen(isOpen);
    }
  }, [isOpen]);

  const animationEndHandler = () => {
    if (canCloseSidebar) {
      setInternalIsOpen(false);
      setCanCloseSidebar(false);
    }
  };

  if (!internalIsOpen) {
    return null;
  }

  return (
    <div
      className={cn(styles.sidebarContainer, { [styles.close]: canCloseSidebar })}
      onAnimationEnd={animationEndHandler}
    >
      <BackButton onClose={onOutsideClick} />
      <div className={styles.void} onClick={onOutsideClick} role="presentation" />
      <div className={styles.contentWrapper}>{children}</div>
    </div>
  );
};
