import { ReactNode, useEffect, useState } from 'react';
import cn from 'classnames';
import ReactDOM from 'react-dom';
import styles from './ModalPage.module.scss';
import { BackButton } from '../BackButton/BackButton';

interface ModalPageProps {
  isOpen: boolean;
  children: ReactNode;
  onClose: VoidFunction;
  onAfterClose?: VoidFunction;
}

const PORTAL = document.body;

export const ModalPage = ({ isOpen, onClose, onAfterClose, children }: ModalPageProps) => {
  const [internalIsOpen, setInternalIsOpen] = useState(false);
  const [canCloseSidebar, setCanCloseSidebar] = useState(false);

  useEffect(() => {
    if (isOpen) {
      PORTAL.style.overflow = 'hidden';

      return () => {
        PORTAL.style.overflow = 'visible';
      };
    }
  }, [isOpen]);

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
      onAfterClose?.();
    }
  };

  if (!internalIsOpen) {
    return null;
  }

  return ReactDOM.createPortal(
    <div
      className={cn(styles.modalContainer, { [styles.close]: canCloseSidebar })}
      onAnimationEnd={animationEndHandler}
    >
      <BackButton onClose={onClose} />
      <div className={styles.contentWrapper}>{children}</div>
    </div>,
    PORTAL,
  );
};
