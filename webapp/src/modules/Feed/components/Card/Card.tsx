import { MouseEvent, TouchEvent, useCallback, useEffect, useMemo, useRef, useState } from 'react';
import cn from 'classnames';
import { BatchI, CustomErrorI } from '../../../../utils/interfaces';
import { SwipeState } from '../../../../utils/constants';
import { useAppDispatch, useAppSelector } from '../../../../utils/hooks/useRedux';
import { useGetDeckPostQuery, useSetLikePostMutation, useSkipPostMutation } from '../../../../redux/api/cheerApi';
import styles from './Card.module.scss';
import { feedSlice } from '../../store/slice';
import { ReactComponent as SettingIcon } from '../../../../assets/icons/filter.svg';
import { ReactComponent as LocationIcon } from '../../../../assets/icons/location.svg';
import { EmptyBatch } from '../HelperModule/EmptyBatch';
import { CardSkeleton } from './Card.skeleton';
import { MIN_PROFILE_NUMBERS, SWIPE_ROW_THRESHOLD } from '../../utils/constants';
import { Snackbar } from '../../../../UI';
import { SwipeResult } from '../../../../components/SwipeResult/SwipeResult';

export const Card = () => {
  const dispatch = useAppDispatch();
  const {
    addNumberOfCard,
    resetNumberOfCard,
    setCanForceUpdate,
    setFilterIsView,
    addProfilesBatch,
    setNewProfilesBatch,
    removeFirstProfile,
    setImageIsDrag,
    setLateSwipeState,
  } = feedSlice.actions;
  const { numberOfCardsViewed, lateSwipeState, sidebarIsShown, profilesBatch, canForceUpdate } = useAppSelector(
    (state) => state.feedReducer,
  );
  const { data: deckData, refetch: refetchDeck } = useGetDeckPostQuery();
  const [setLike] = useSetLikePostMutation();
  const [setDislike] = useSkipPostMutation();

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<CustomErrorI | null>(null);
  const [canSwipeAnimation, setCanSwipeAnimation] = useState(false);
  const [swipeState, setSwipeState] = useState<SwipeState>(SwipeState.nothing);
  const [swipeLighting, setSwipeLighting] = useState<SwipeState>(SwipeState.nothing);
  const [currentX, setCurrentX] = useState(0);
  const [startX, setStartX] = useState<number | null>(null);
  const [currentPhotoNumber, setCurrentPhotoNumber] = useState(0);
  const isUpdateEvent = useRef(false);
  const imageRef = useRef<HTMLDivElement>(null);

  const generateCards = useCallback(
    async (batch: BatchI[]) => {
      try {
        setError(null);
        setIsLoading(true);
        const templateBatch: BatchI[] = [];

        for (const [profileIndex, profile] of batch.entries()) {
          const promises = profile.photos.map((photo) => fetch(`https://cdn.lovolab.ru/${photo.url}`));
          const responses = await Promise.all(promises);
          const imagesPromise = responses.map((image) => image.blob());
          const images = await Promise.all(imagesPromise);
          templateBatch.push(structuredClone(profile));

          images.forEach((image, imageIndex) => {
            templateBatch[profileIndex].photos[imageIndex].url = URL.createObjectURL(image);
          });
        }

        if (canForceUpdate) {
          dispatch(setNewProfilesBatch(templateBatch));
          dispatch(setCanForceUpdate(false));
        } else {
          dispatch(addProfilesBatch(templateBatch.slice(numberOfCardsViewed)));
        }
      } catch (err) {
        setError(err as CustomErrorI);
        console.error('Ошибка загрузки изображений', err);
      } finally {
        setIsLoading(false);
      }
    },
    [canForceUpdate],
  );

  useEffect(() => {
    if (deckData?.batch && !profilesBatch.length) {
      generateCards(deckData.batch);
    }
  }, []);

  useEffect(() => {
    const getDeck = async () => {
      const { batch } = await refetchDeck().unwrap();
      await generateCards(batch);
      dispatch(resetNumberOfCard());
    };
    const canUpdate =
      !isLoading &&
      profilesBatch.length <= MIN_PROFILE_NUMBERS &&
      deckData?.batch.length === 5 &&
      isUpdateEvent.current;

    if (canUpdate || canForceUpdate) {
      getDeck();
    }

    return () => {
      isUpdateEvent.current = true;
    };
  }, [profilesBatch, canForceUpdate]);

  const currentProfile = useMemo(() => profilesBatch[0], [profilesBatch]);

  const openFilterHandler = useCallback((e: MouseEvent<HTMLDivElement>) => {
    e.stopPropagation();
    dispatch(setFilterIsView(true));
  }, []);

  const swipeHandler = useCallback(
    (state: SwipeState) => {
      if (state === SwipeState.like) {
        setCurrentX(700);
        setLike(profilesBatch[0].id);
        setSwipeState(state);
      } else if (state === SwipeState.skip) {
        setCurrentX(-700);
        setDislike(profilesBatch[0].id);
        setSwipeState(state);
      }
    },
    [profilesBatch],
  );

  useEffect(() => {
    if (!sidebarIsShown && lateSwipeState) {
      swipeHandler(lateSwipeState);
      setSwipeLighting(lateSwipeState);
    }
  }, [sidebarIsShown, lateSwipeState]);

  const cardTouchStartHandler = useCallback((e: TouchEvent<HTMLDivElement>) => {
    e.stopPropagation();

    if (e.target !== imageRef.current) {
      return;
    }

    setStartX(e.targetTouches[0].clientX);
    dispatch(setImageIsDrag(true));
  }, []);

  const cardTouchMoveHandler = useCallback(
    (e: TouchEvent<HTMLDivElement>) => {
      e.stopPropagation();

      if (e.target !== imageRef.current || startX === null) {
        return;
      }

      const x = -(startX - e.targetTouches[0].clientX);
      setCurrentX(x);

      if (x > SWIPE_ROW_THRESHOLD) {
        setSwipeLighting(SwipeState.like);
      } else if (Math.abs(x) > SWIPE_ROW_THRESHOLD) {
        setSwipeLighting(SwipeState.skip);
      } else {
        setSwipeLighting(SwipeState.nothing);
      }
    },
    [startX],
  );

  const cardTouchEndHandler = useCallback(
    (e: TouchEvent<HTMLDivElement>) => {
      e.stopPropagation();

      if (currentX === 0) {
        return;
      }

      if (currentX > SWIPE_ROW_THRESHOLD) {
        swipeHandler(SwipeState.like);
      } else if (Math.abs(currentX) > SWIPE_ROW_THRESHOLD) {
        swipeHandler(SwipeState.skip);
      } else {
        swipeHandler(SwipeState.nothing);
        setCanSwipeAnimation(true);
        setCurrentX(0);
      }

      setStartX(null);
    },
    [currentX],
  );

  const informationAnimationHandler = useCallback(() => {
    if (lateSwipeState) {
      dispatch(setLateSwipeState(SwipeState.nothing));
    }

    if (swipeState) {
      setCurrentPhotoNumber(0);
      dispatch(removeFirstProfile());
      setSwipeState(SwipeState.nothing);
      setCurrentX(0);
      dispatch(addNumberOfCard());
    }

    setCanSwipeAnimation(false);
    dispatch(setImageIsDrag(false));
    setSwipeLighting(SwipeState.nothing);
  }, [swipeState]);

  const changePhotoHandler = useCallback(
    (e: MouseEvent<HTMLDivElement>) => {
      e.stopPropagation();
      dispatch(setImageIsDrag(false));

      if (e.pageX > window.innerWidth / 2) {
        setCurrentPhotoNumber((prevState) => {
          if (currentProfile.photos.length - 1 > prevState) {
            return prevState + 1;
          }
          return 0;
        });
      } else if (e.pageX < window.innerWidth / 2) {
        setCurrentPhotoNumber((prevState) => {
          if (prevState === 0) {
            return currentProfile.photos.length - 1;
          }
          return prevState - 1;
        });
      }
    },
    [currentProfile],
  );

  const photoLinesComponent = useMemo(() => {
    if (!currentProfile || currentProfile.photos.length <= 1) {
      return null;
    }

    return (
      <>
        {currentProfile.photos.map((profile, index) => (
          <div key={profile.id} className={cn(styles.stepLine, { [styles.active]: currentPhotoNumber === index })} />
        ))}
      </>
    );
  }, [currentProfile, currentPhotoNumber]);

  const swipeResultComponent = useMemo(() => {
    return <SwipeResult swipeState={swipeLighting} />;
  }, [swipeLighting]);

  if ((isLoading && !profilesBatch.length) || canForceUpdate) {
    return <CardSkeleton />;
  }

  if (!profilesBatch.length) {
    return <EmptyBatch />;
  }

  return (
    <>
      <div
        className={cn(styles.cardContainer, {
          [styles.swipeAction]: swipeState !== SwipeState.nothing,
          [styles.back]: canSwipeAnimation,
        })}
        style={{
          transform: `translateX(${currentX}px)`,
        }}
        draggable
        onTouchStart={cardTouchStartHandler}
        onTouchMove={cardTouchMoveHandler}
        onTouchEnd={cardTouchEndHandler}
        onTransitionEnd={informationAnimationHandler}
        onClick={changePhotoHandler}
        role="presentation"
        ref={imageRef}
      >
        <div className={styles.imageWrapper}>
          <img src={currentProfile.photos[currentPhotoNumber].url} alt="profile" />
        </div>
        <div className={styles.filterWrapper}>
          <div className={styles.stepLineWrapper}>{photoLinesComponent}</div>
          <div className={styles.filterButton} onClick={openFilterHandler} role="presentation">
            <SettingIcon />
          </div>
        </div>
        <div className={cn(styles.previewWrapper, styles[swipeLighting])}>
          <div className={styles.preview}>
            <div className={styles.name}>
              {currentProfile.name}
              ,&nbsp;
              {currentProfile.age}
            </div>
            <div className={styles.distance}>
              <LocationIcon />
              &nbsp;&lt;&nbsp;
              {currentProfile.distance}
              &nbsp;км
            </div>
          </div>
        </div>
      </div>
      {swipeResultComponent}
      <Snackbar shouldRender={!!error} description={error ?? ''} />
    </>
  );
};
