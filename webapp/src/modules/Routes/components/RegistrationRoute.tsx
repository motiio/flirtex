import { Navigate, Outlet } from 'react-router-dom';
import { useEffect } from 'react';
import WebApp from '@twa-dev/sdk';
import { useAppSelector } from '../../../utils/hooks/useRedux';

export const RegistrationRoute = () => {
  const { hasProfile } = useAppSelector((state) => state.authReducer);

  useEffect(() => {
    WebApp.SettingsButton.hide();
  }, []);

  if (hasProfile === null) {
    return <Navigate to="/404" replace />;
  }

  if (hasProfile) {
    return <Navigate to="/feed" replace />;
  }

  return <Outlet />;
};
