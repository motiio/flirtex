import { useState } from 'react';
import { ModalPage } from '../../../../components/ModalPage/ModalPage';
import { useAppDispatch, useAppSelector } from '../../../../utils/hooks/useRedux';
import { interactionSlice } from '../../store/slice';
import { useGetProfileByIdGetQuery, useSetLikePostMutation, useSkipPostMutation } from '../../../../redux/api/cheerApi';
import styles from './Modal.module.scss';
import { ErrorComponent } from '../../../../components/ErrorComponent/ErrorComponent';
import { StickyMenu } from '../../../../components/StickyMenu/StickyMenu';
import { stickyMenu } from '../../utils/config';
import { SwipeState } from '../../../../utils/constants';
import { SwipeResult } from '../../../../components/SwipeResult/SwipeResult';
import { Profile } from '../../../../components/Profile/Profile';
import { ProfileSkeleton } from '../../../../components/Profile/Profile.skeleton';

export const Modal = () => {
  const dispatch = useAppDispatch();
  const { setIsShownModal, removeProfileFromLikeReactions } = interactionSlice.actions;
  const { profileId, isShownModal } = useAppSelector((state) => state.interactionReducer);
  const [swipeState, setSwipeState] = useState<SwipeState>(SwipeState.nothing);
  const [canShownSwipeAnimation, setCanShownSwipeAnimation] = useState(false);

  const {
    data: profile,
    isFetching,
    error,
    refetch,
  } = useGetProfileByIdGetQuery(profileId, { skip: profileId === '' });
  const [setLike] = useSetLikePostMutation();
  const [setDislike] = useSkipPostMutation();

  const closeHandler = () => {
    dispatch(setIsShownModal(false));
  };

  const stickActionHandler = (state: SwipeState) => {
    if (state === SwipeState.like) {
      setLike(profileId);
    } else if (state === SwipeState.skip) {
      setDislike(profileId);
    }

    setSwipeState(state);
    closeHandler();
  };

  const afterCloseHandler = () => {
    if (swipeState) {
      setCanShownSwipeAnimation(true);

      setTimeout(() => {
        setSwipeState(SwipeState.nothing);
        dispatch(removeProfileFromLikeReactions(profileId));
      }, 500);
    }
  };

  return (
    <>
      <ModalPage isOpen={isShownModal} onClose={closeHandler} onAfterClose={afterCloseHandler}>
        <div className={styles.modalContainer}>
          {isFetching && <ProfileSkeleton />}
          {error && (
            <div className={styles.errorWrapper}>
              <ErrorComponent onClick={refetch} error={error} />
            </div>
          )}
          {profile && !isFetching && <Profile profile={profile} />}
        </div>
        {!error && (
          <StickyMenu
            isDisplayed={!isFetching}
            config={stickyMenu}
            onClick={stickActionHandler}
            className={styles.customStickyMenu}
          />
        )}
      </ModalPage>
      <SwipeResult swipeState={canShownSwipeAnimation ? swipeState : SwipeState.nothing} />
    </>
  );
};
