import { useEffect, useRef, useState } from 'react';
import styles from './Cards.module.scss';
import { useIntersectionObserver } from '../../../../utils/hooks/useIntersectionObserver';
import { useGetLikeReactionGetQuery } from '../../../../redux/api/cheerApi';
import { Loader } from '../../../../UI';
import { Modal } from '../Modal/Modal';
import { useAppDispatch, useAppSelector } from '../../../../utils/hooks/useRedux';
import { interactionSlice } from '../../store/slice';
import { ErrorComponent } from '../../../../components/ErrorComponent/ErrorComponent';
import { CardsSkeleton } from './Cards.skeleton';
import { EmptyCard } from '../EmptyCard/EmptyCard';
import { Card } from '../Card/Card';

export const Cards = () => {
  const [hasNextPage, setHasNextPage] = useState(true);
  const dispatch = useAppDispatch();
  const { setPage, reset } = interactionSlice.actions;
  const { page, likeReactions } = useAppSelector((state) => state.interactionReducer);
  const pageRef = useRef(page);

  const {
    isLoading: likeIsLoading,
    isFetching: likeIsFetching,
    error: likeError,
    refetch,
  } = useGetLikeReactionGetQuery({ page });

  useEffect(() => {
    return () => {
      dispatch(reset());
    };
  }, []);

  const getNextPage = () => {
    if (!likeReactions) return;

    const { total, limit, offset } = likeReactions.pagination;

    if (total <= offset + limit) {
      setHasNextPage(false);
    } else {
      pageRef.current = page + 1;
      dispatch(setPage(page + 1));
    }
  };

  const observerRef = useIntersectionObserver<HTMLDivElement>(getNextPage, [hasNextPage, !likeIsFetching]);

  if (likeError) {
    return <ErrorComponent error={likeError} onClick={refetch} isWrongPage />;
  }

  if (likeIsLoading) {
    return <CardsSkeleton />;
  }

  if (!likeReactions?.profiles.length) {
    return <EmptyCard />;
  }

  return (
    <div className={styles.cardsContainer}>
      {likeReactions.profiles.map((profile) => (
        <Card key={profile.id} profile={profile} />
      ))}
      {likeIsFetching && (
        <div className={styles.loaderWrapper}>
          <Loader className={styles.loader} size="S" />
        </div>
      )}
      <div ref={observerRef} className={styles.observer} />
      <Modal />
    </div>
  );
};
