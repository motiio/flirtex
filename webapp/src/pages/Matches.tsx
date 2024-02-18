import { useEffect } from 'react';
import WebApp from '@twa-dev/sdk';
import { MatchesModule } from '../modules/Matches';

const Matches = () => {
  useEffect(() => {
    WebApp.MainButton.hide();
  }, []);

  return <MatchesModule />;
};

export default Matches;
