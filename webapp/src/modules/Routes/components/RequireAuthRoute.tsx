import { Navigate, Outlet } from 'react-router-dom';
import { useEffect } from 'react';
import WebApp from '@twa-dev/sdk';
import { useAppDispatch, useAppSelector } from '../../../utils/hooks/useRedux';
import { useLazyGetMyProfileProfileGetQuery, useLoginUserAuthPostMutation } from '../../../redux/api/cheerApi';
import { AppLoad } from '../../../components/AppLoad/AppLoad';
import { ErrorComponent } from '../../../components/ErrorComponent/ErrorComponent';
import { WithoutTelegram } from './WithoutTelegram/WithoutTelegram';
import { authSlice } from '../../../redux/feature/authSlice';

const USER_TOKEN = WebApp.initData;

export const RequireAuth = () => {
  const dispatch = useAppDispatch();
  const { accessToken, hasProfile, refreshToken } = useAppSelector((state) => state.authReducer);
  const { addProfileId } = authSlice.actions;
  const [firstAuth, { isLoading: authIsLoading, isError, error: authError }] = useLoginUserAuthPostMutation();
  const [getProfile, { isLoading: profileIsLoading, error: profileError, isUninitialized }] =
    useLazyGetMyProfileProfileGetQuery();

  // TODO  isLoading govno
  const isLoading = authIsLoading || profileIsLoading || isUninitialized || hasProfile === null;

  useEffect(() => {
    const idRegex = /"id":(\d+)/;
    const idResult = decodeURIComponent(WebApp.initData).match(idRegex);
    const profileId = idResult ? idResult[1] : '000';

    dispatch(addProfileId(profileId));
  }, []);

  useEffect(() => {
    WebApp.enableClosingConfirmation();
    WebApp.MainButton.hideProgress();

    if (!WebApp.isExpanded) {
      WebApp.expand();
    }
  }, []);

  useEffect(() => {
    if (hasProfile === null && !refreshToken && !!USER_TOKEN) {
      firstAuth({
        userAgent: 'USER_TOKEN',
        userLoginRequest: { initData: USER_TOKEN },
      });
    }
  }, [hasProfile, refreshToken]);

  useEffect(() => {
    if (accessToken) {
      getProfile();
    }
  }, [accessToken]);
  // вроде неправильно

  if (!USER_TOKEN && !refreshToken) {
    return <WithoutTelegram />;
  }

  if (isLoading) {
    return <AppLoad />;
  }

  if (profileError) {
    if ('status' in profileError && profileError.status === 404) {
      return <Navigate to="/registration" replace />;
    }
  }

  if (isError || profileError) {
    return <ErrorComponent isWrongPage error={authError ?? profileError} />;
  }

  if (isLoading) {
    return <AppLoad />;
  }

  return <Outlet />;
};
