import { useEffect } from 'react';
import WebApp from '@twa-dev/sdk';
import { ProfileModule } from '../modules/Profile';

const Profile = () => {
  useEffect(() => {
    WebApp.MainButton.hide();
  }, []);

  return <ProfileModule />;
};

export default Profile;
