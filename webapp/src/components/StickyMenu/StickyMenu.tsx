import ReactDOM from 'react-dom';
import cn from 'classnames';
import { FunctionComponent, useEffect, useRef } from 'react';
import styles from './StickyMenu.module.scss';

interface StickyMenuProps<T> {
  isDisplayed: boolean;
  config: { value: T; Icon: FunctionComponent }[];
  onClick: (value: T) => void;
  className?: string;
}

export function StickyMenu<T>({ isDisplayed, config, onClick, className }: StickyMenuProps<T>) {
  const portalRef = useRef(document.body);

  useEffect(() => {
    const rootPortal = document.getElementById('root');

    if (rootPortal) {
      portalRef.current = rootPortal;
    }
  }, []);

  if (!isDisplayed) {
    return null;
  }

  const clickHandler = (value: T) => {
    onClick(value);
  };

  return ReactDOM.createPortal(
    <div className={cn(styles.sticky, className)}>
      <div className={styles.actionMenuWrapper}>
        {config.map(({ value, Icon }) => (
          <div
            key={value as string}
            className={cn(styles.action, styles[value as string])}
            onClick={() => clickHandler(value)}
            role="presentation"
          >
            <Icon />
          </div>
        ))}
      </div>
    </div>,
    portalRef.current,
  );
}
