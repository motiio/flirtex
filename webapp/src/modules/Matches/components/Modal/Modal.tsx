import { useAppDispatch, useAppSelector } from '../../../../utils/hooks/useRedux';
import { matchesSlice } from '../../store/slice';
import { useGetProfileByIdGetQuery } from '../../../../redux/api/cheerApi';
import styles from './Modal.module.scss';
import { ErrorComponent } from '../../../../components/ErrorComponent/ErrorComponent';
import { ModalPage } from '../../../../components/ModalPage/ModalPage';
import { Profile } from '../../../../components/Profile/Profile';
import { ProfileSkeleton } from '../../../../components/Profile/Profile.skeleton';

export const Modal = () => {
  const dispatch = useAppDispatch();
  const { setIsShownModal } = matchesSlice.actions;
  const { profileId, isShownModal } = useAppSelector((state) => state.matchesReducer);
  const {
    data: profile,
    isFetching,
    error,
    refetch,
  } = useGetProfileByIdGetQuery(profileId, { skip: profileId === '' });

  const closeHandler = () => {
    dispatch(setIsShownModal(false));
  };

  return (
    <ModalPage isOpen={isShownModal} onClose={closeHandler}>
      <div className={styles.modalContainer}>
        {isFetching && <ProfileSkeleton />}
        {error && (
          <div className={styles.errorWrapper}>
            <ErrorComponent onClick={refetch} error={error} />
          </div>
        )}
        {profile && !isFetching && <Profile profile={profile} />}
      </div>
    </ModalPage>
  );
};
