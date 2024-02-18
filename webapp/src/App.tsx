import { Navigate, Route, Routes, useLocation } from 'react-router-dom';
import { useEffect } from 'react';
import WebApp from '@twa-dev/sdk';
import Registration from './pages/Registration';
import Feed from './pages/Feed';
import Matches from './pages/Matches';
import Interaction from './pages/Interaction';
import Profile from './pages/Profile';
import Page404 from './pages/404';
import { AppCoverModule } from './modules/AppCover';
import { RegistrationRoute, RequireAuth } from './modules/Routes';
import { PagesLink } from './utils/constants';

const App = () => {
  const { pathname } = useLocation();

  useEffect(() => {
    WebApp.ready();
  }, []);

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);

  return (
    <Routes>
      <Route element={<RegistrationRoute />}>
        <Route path={PagesLink.registration} element={<Registration />} />
      </Route>
      <Route element={<RequireAuth />}>
        <Route element={<AppCoverModule />}>
          <Route path={PagesLink.feed} element={<Feed />} />
          <Route path={PagesLink.matches} element={<Matches />} />
          <Route path={PagesLink.interaction} element={<Interaction />} />
          <Route path={PagesLink.profile} element={<Profile />} />
          <Route path={PagesLink.default} element={<Navigate to={PagesLink.feed} replace />} />
        </Route>
      </Route>
      <Route path="*" element={<Page404 />} />
    </Routes>
  );
};

export default App;
