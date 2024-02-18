import { NavLink } from 'react-router-dom';
import cn from 'classnames';
import WebApp from '@twa-dev/sdk';
import styles from './BottomNavigation.module.scss';
import { bottomNavigationConfig } from '../../utils/config';

export const BottomNavigation = () => {
  const clickHandler = () => {
    if (WebApp.platform !== 'unknown') {
      WebApp.HapticFeedback.notificationOccurred('success');
    }
  };

  return (
    <div className={styles.navigationWrapper}>
      <div className={styles.line} />
      <div className={styles.linksWrapper}>
        {bottomNavigationConfig.map(({ page, Icon }) => (
          <NavLink
            key={page}
            to={page}
            className={({ isActive }) => cn({ [styles.selected]: isActive })}
            onClick={clickHandler}
          >
            <Icon />
          </NavLink>
        ))}
      </div>
    </div>
  );
};
