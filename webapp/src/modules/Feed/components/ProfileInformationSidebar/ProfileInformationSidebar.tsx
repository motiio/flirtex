import { TouchEvent, useCallback, useEffect, useRef, useState } from 'react';
import cn from 'classnames';
import styles from './ProfileInformationSidebar.module.scss';
import { Animation, SWIPE_SIDEBAR_THRESHOLD } from '../../utils/constants';
import { ProfileInfo } from '../ProfileInfo/ProfileInfo';
import { ReactComponent as SortIcon } from '../../../../assets/icons/sort.svg';
import { SwipeState } from '../../../../utils/constants';
import { useAppDispatch, useAppSelector } from '../../../../utils/hooks/useRedux';
import { feedSlice } from '../../store/slice';
import { StickyMenu } from '../../../../components/StickyMenu/StickyMenu';
import { stickyMenu } from '../../utils/config';
import { BackButton } from '../../../../components/BackButton/BackButton';

export const ProfileInformationSidebar = () => {
  const dispatch = useAppDispatch();
  const { setSidebarIsShown, setLateSwipeState } = feedSlice.actions;
  const { sidebarIsShown, imageIsDrag, profilesBatch } = useAppSelector((state) => state.feedReducer);

  const [barOverflowIsShown, setBarOverflowIsShown] = useState(false);
  const [stickySwipeResult, setStickySwipeResult] = useState<SwipeState>(SwipeState.nothing);
  const [animation, setAnimation] = useState<Animation>(Animation.none);
  const [offsetY, setOffsetY] = useState(0);
  const [startY, setStartY] = useState<number | null>(null);
  const swipePlaceRef = useRef<HTMLDivElement>(null);
  const barRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setOffsetY(window.innerHeight - 148);

    return () => {
      dispatch(setSidebarIsShown(false));
    };
  }, []);

  useEffect(() => {
    if (sidebarIsShown) {
      return () => {
        barRef.current?.scrollTo({ top: 0, behavior: 'smooth' });
      };
    }
  }, [sidebarIsShown]);

  useEffect(() => {
    const handleTouchMove = (e: globalThis.TouchEvent) => {
      e.preventDefault();
    };
    const element = swipePlaceRef.current;

    if (element) {
      element.addEventListener('touchmove', handleTouchMove, { passive: false });

      return () => {
        element.removeEventListener('touchmove', handleTouchMove);
      };
    }
  }, [startY, offsetY]);

  const barTouchStartHandler = useCallback((e: TouchEvent<HTMLDivElement>) => {
    e.stopPropagation();

    if (e.target !== swipePlaceRef.current) {
      return;
    }

    setStartY(e.targetTouches[0].clientY);
  }, []);

  const barTouchMoveHandler = useCallback(
    (e: TouchEvent<HTMLDivElement>) => {
      e.stopPropagation();

      if (startY === null) {
        return;
      }
      setOffsetY(e.targetTouches[0].clientY - 78);
    },
    [sidebarIsShown, startY],
  );

  const barTouchEndHandler = useCallback(
    (e: TouchEvent<HTMLDivElement>) => {
      e.stopPropagation();

      if (startY === null) {
        return;
      }

      if (startY - offsetY > SWIPE_SIDEBAR_THRESHOLD) {
        dispatch(setSidebarIsShown(true));
        setOffsetY(-100);
        setAnimation(Animation.open);
      } else if (offsetY - startY > SWIPE_SIDEBAR_THRESHOLD) {
        dispatch(setSidebarIsShown(false));
        setOffsetY(window.innerHeight - 48);
        setAnimation(Animation.close);
      } else if (sidebarIsShown) {
        setOffsetY(-100);
        setAnimation(Animation.open);
      } else {
        setOffsetY(window.innerHeight - 48);
        setAnimation(Animation.close);
      }

      setStartY(null);
    },
    [startY, offsetY],
  );

  const closeProfileHandler = () => {
    if (sidebarIsShown) {
      dispatch(setSidebarIsShown(false));
      setOffsetY(window.innerHeight - 48);
      setAnimation(Animation.close);
    } else {
      dispatch(setSidebarIsShown(true));
      setOffsetY(-100);
      setAnimation(Animation.open);
    }
  };

  const transitionEndHandler = () => {
    setAnimation(Animation.none);

    if (sidebarIsShown) {
      setOffsetY(0);
      setBarOverflowIsShown(true);
    } else {
      setOffsetY(window.innerHeight - 148);
      setBarOverflowIsShown(false);
    }

    if (stickySwipeResult) {
      dispatch(setLateSwipeState(stickySwipeResult));
      setStickySwipeResult(SwipeState.nothing);
    }
  };

  const closeProfileWithActionHandler = (state: SwipeState) => {
    closeProfileHandler();
    setStickySwipeResult(state);
  };

  return (
    <div
      className={cn(styles.sidebarContainer, styles[animation], {
        [styles.active]: barOverflowIsShown,
        [styles.hidden]: imageIsDrag || !profilesBatch.length,
      })}
      style={{ transform: `translateY(${offsetY}px)` }}
      onTransitionEnd={transitionEndHandler}
      ref={barRef}
    >
      {!barOverflowIsShown && (
        <div
          className={styles.closeButton}
          draggable
          onTouchStart={barTouchStartHandler}
          onTouchMove={barTouchMoveHandler}
          onTouchEnd={barTouchEndHandler}
          onClick={closeProfileHandler}
          role="presentation"
          ref={swipePlaceRef}
        >
          <SortIcon />
        </div>
      )}
      <div className={styles.contentWrapper} onClick={closeProfileHandler} role="presentation">
        <ProfileInfo />
      </div>
      <StickyMenu isDisplayed={sidebarIsShown} config={stickyMenu} onClick={closeProfileWithActionHandler} />
      {sidebarIsShown && <BackButton onClose={closeProfileHandler} />}
    </div>
  );
};
