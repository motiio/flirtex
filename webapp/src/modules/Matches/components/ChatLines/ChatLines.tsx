import { useEffect, useRef, useState } from 'react';
import { useGetMatchesGetQuery } from '../../../../redux/api/cheerApi';
import { useAppDispatch, useAppSelector } from '../../../../utils/hooks/useRedux';
import styles from './ChatLines.module.scss';
import { matchesSlice } from '../../store/slice';
import { ErrorComponent } from '../../../../components/ErrorComponent/ErrorComponent';
import { ChatLinesSkeleton } from './ChatLines.skeleton';
import { EmptyCard } from '../EmptyCard/EmptyCard';
import { ChatLine } from '../ChatLine/ChatLine';
import { useIntersectionObserver } from '../../../../utils/hooks/useIntersectionObserver';
import { Loader } from '../../../../UI';

export const ChatLines = () => {
  const dispatch = useAppDispatch();
  const { setPage, reset } = matchesSlice.actions;
  const { page } = useAppSelector((state) => state.matchesReducer);
  const [hasNextPage, setHasNextPage] = useState(true);
  const pageRef = useRef(page);

  const {
    data: matches,
    isLoading: matchesIsLoading,
    isFetching: matchesIsFetching,
    error: likeError,
    refetch,
  } = useGetMatchesGetQuery({ page, limit: 15 });

  useEffect(() => {
    return () => {
      reset();
    };
  }, []);

  useEffect(() => {
    if (matches && pageRef.current !== matches.pagination.offset / 15) {
      pageRef.current = 0;
      dispatch(setPage(0));
    }
  }, [matches]);

  const getNextPage = () => {
    if (!matches) return;

    const { total, limit, offset } = matches.pagination;

    if (total <= offset + limit) {
      setHasNextPage(false);
    } else {
      pageRef.current = page + 1;
      dispatch(setPage(page + 1));
    }
  };

  const observerRef = useIntersectionObserver<HTMLDivElement>(getNextPage, [hasNextPage, !matchesIsFetching]);

  if (likeError) {
    return <ErrorComponent error={likeError} onClick={refetch} isWrongPage />;
  }

  if (matchesIsLoading) {
    return <ChatLinesSkeleton />;
  }

  if (!matches?.profiles.length) {
    return <EmptyCard />;
  }

  return (
    <div className={styles.chatLineContainer}>
      {matches.profiles.map((profile) => (
        <ChatLine key={profile.profile_id} profile={profile} />
      ))}
      {matchesIsFetching && (
        <div className={styles.loaderWrapper}>
          <Loader className={styles.loader} size="S" />
        </div>
      )}
      <div ref={observerRef} className={styles.observer} />
    </div>
  );
};
