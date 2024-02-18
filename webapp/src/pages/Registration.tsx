import { useEffect } from 'react';
import WebApp from '@twa-dev/sdk';
import { RegistrationModule } from '../modules/Registration';

const Registration = () => {
  useEffect(() => {
    WebApp.MainButton.show();
  }, []);

  return <RegistrationModule />;
};

export default Registration;
