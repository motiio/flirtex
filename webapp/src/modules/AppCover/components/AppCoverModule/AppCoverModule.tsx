import { Outlet } from 'react-router-dom';
import cn from 'classnames';
import { useEffect } from 'react';
import WebApp from '@twa-dev/sdk';
import styles from './AppCoverModule.module.scss';
import { BottomNavigation } from '../BottomNavigation/BottomNavigation';
import { SettingsModal } from '../SettingsModal/SettingsModal';
import { useAppDispatch, useAppSelector } from '../../../../utils/hooks/useRedux';
import { ProfileModal } from '../ProfileModal/ProfileModal';
import { appCoverSlice } from '../../store/slice';

export const AppCoverModule = () => {
  const { settingsIsShown } = useAppSelector((state) => state.appCoverReducer);
  const dispatch = useAppDispatch();
  const { setProfileId, setProfileIsShown } = appCoverSlice.actions;

  useEffect(() => {
    const startParam = WebApp.initDataUnsafe.start_param?.split('-idp');

    if (startParam?.length === 2) {
      dispatch(setProfileId(startParam[0]));
      dispatch(setProfileIsShown(true));
    }
  }, []);

  return (
    <>
      <div className={cn(styles.appCoverModuleContainer, { [styles.disabled]: settingsIsShown })}>
        <Outlet />
        <SettingsModal />
      </div>
      <BottomNavigation />
      <ProfileModal />
    </>
  );
};
