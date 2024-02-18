import cn from 'classnames';
import { useEffect, useState } from 'react';
import ReactDOM from 'react-dom';
import { ErrorT } from '../../utils/interfaces';
import styles from './Snackbar.module.scss';
import { ReactComponent as ErrorIcon } from '../../assets/icons/close-circle.svg';
import { ReactComponent as SuccessIcon } from '../../assets/icons/tick-circle.svg';
import { ReactComponent as InfoIcon } from '../../assets/icons/danger.svg';

type AlertColorT = 'success' | 'info' | 'error';

interface SnackbarProps {
  shouldRender: boolean;
  description?: ErrorT;
  label?: string;
  closeText?: string;
  type?: AlertColorT;
  hasNavigationBar?: boolean;
  onClose?: () => void;
}

export const Snackbar = ({
  shouldRender,
  label,
  description,
  closeText,
  onClose,
  type = 'error',
  hasNavigationBar = true,
}: SnackbarProps) => {
  const [portal, setPortal] = useState(document.body);
  const [text, setText] = useState('Неизвестная ошибка');
  const [isOpen, setIsOpen] = useState(false);
  const [canHidden, setCanHidden] = useState(false);

  useEffect(() => {
    const rootPortal = document.getElementById('mode-toggle');

    if (rootPortal) {
      setPortal(rootPortal);
    }
  }, []);

  useEffect(() => {
    setIsOpen(shouldRender);

    if (shouldRender) {
      const timer = setTimeout(() => {
        setCanHidden(true);
      }, 4000);

      return () => clearTimeout(timer);
    }
  }, [shouldRender]);

  // передаем error из redux и забываем обо всем
  useEffect(() => {
    if (!description) {
      setText('Неизвестная ошибка');
    } else if (typeof description === 'string') {
      setText(description);
    } else if ('data' in description && 'status' in description) {
      if (description.data.detail instanceof Array) {
        setText(description.data.detail[0].msg);
      } else {
        setText(description.data.detail.msg);
      }
    } else if ('message' in description) {
      setText(description.message || 'Неизвестная ошибка');
    } else {
      setText('Неизвестная ошибка');
    }
  }, [description]);

  const closeHandler = () => {
    setIsOpen(false);

    if (onClose) {
      onClose();
    }
  };

  const animationEndHandler = () => {
    if (canHidden) {
      setCanHidden(false);
      closeHandler();
    }
  };

  if (!isOpen) return null;

  return ReactDOM.createPortal(
    <div
      className={cn(styles.container, { [styles.hidden]: canHidden, [styles.withoutNavigation]: !hasNavigationBar })}
      onClick={closeHandler}
      onAnimationEnd={animationEndHandler}
      role="presentation"
    >
      <div className={styles.alert}>
        <div className={cn(styles.icon, styles[type])}>
          {type === 'info' && <InfoIcon />}
          {type === 'success' && <SuccessIcon />}
          {type === 'error' && <ErrorIcon />}
        </div>
        <div>
          {label && <div className={styles.label}>{label}</div>}
          <div className={styles.description}>{text}</div>
        </div>
        {closeText && <div className={styles.closeText}>{closeText}</div>}
      </div>
    </div>,
    portal,
  );
};
