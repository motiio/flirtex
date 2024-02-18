import { useEffect } from 'react';
import { useGetDeckPostQuery, useGetMyProfileProfileGetQuery } from '../../../../redux/api/cheerApi';
import { EmptyProfile } from '../HelperModule/EmptyProfile';
import { Card } from '../Card/Card';
import styles from './FeedModule.module.scss';
import { ErrorComponent } from '../../../../components/ErrorComponent/ErrorComponent';
import { CardSkeleton } from '../Card/Card.skeleton';
import { useAppDispatch, useAppSelector } from '../../../../utils/hooks/useRedux';
import { feedSlice } from '../../store/slice';
import { CardsCollection } from '../CardsCollection/CardsCollection';
import { ProfileInformationSidebar } from '../ProfileInformationSidebar/ProfileInformationSidebar';
import { FilterSidebar } from '../FilterSidebar/FilterSidebar';

export const FeedModule = () => {
  const { data: profile, isLoading: profileIsLoading, error: profileError } = useGetMyProfileProfileGetQuery();
  const { isLoading: deckIsLoading, error: deckError } = useGetDeckPostQuery();
  const dispatch = useAppDispatch();
  const { reset } = feedSlice.actions;
  const { profilesBatch, canForceUpdate } = useAppSelector((state) => state.feedReducer);

  useEffect(() => {
    return () => {
      dispatch(reset());
    };
  }, []);

  if (!profile || profileError) {
    return <ErrorComponent error={profileError} />;
  }

  if (deckError) {
    return <ErrorComponent error={deckError} />;
  }

  if (deckIsLoading || profileIsLoading) {
    return <CardSkeleton />;
  }

  if (!profile.has_location || !profile.photos.length) {
    return <EmptyProfile distanceIsEmpty={!profile.has_location} photosIsEmpty={!profile.photos.length} />;
  }

  return (
    <div className={styles.feedContainer}>
      <Card />
      {!!profilesBatch.length && !canForceUpdate && <CardsCollection profiles={profilesBatch.slice(1)} />}
      <FilterSidebar />
      {!canForceUpdate && !!profilesBatch.length && <ProfileInformationSidebar />}
    </div>
  );
};
