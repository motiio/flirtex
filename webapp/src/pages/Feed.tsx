import { useEffect } from 'react';
import WebApp from '@twa-dev/sdk';
import { FeedModule } from '../modules/Feed';

const Feed = () => {
  useEffect(() => {
    WebApp.MainButton.hide();
  }, []);

  return <FeedModule />;
};

export default Feed;
