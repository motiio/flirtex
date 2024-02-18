import { useEffect } from 'react';
import WebApp from '@twa-dev/sdk';
import { InteractionModule } from '../modules/Interaction';

const Interaction = () => {
  useEffect(() => {
    WebApp.MainButton.hide();
  }, []);

  return <InteractionModule />;
};

export default Interaction;
