import { ModalPage } from '../../../../components/ModalPage/ModalPage';
import { useAppDispatch, useAppSelector } from '../../../../utils/hooks/useRedux';
import { appCoverSlice } from '../../store/slice';
import { Profile } from '../../../../components/Profile/Profile';
import { useGetProfileByIdGetQuery } from '../../../../redux/api/cheerApi';
import styles from '../../../Interaction/components/Modal/Modal.module.scss';
import { ProfileSkeleton } from '../../../../components/Profile/Profile.skeleton';
import { ErrorComponent } from '../../../../components/ErrorComponent/ErrorComponent';

export const ProfileModal = () => {
  const dispatch = useAppDispatch();
  const { setProfileIsShown, setProfileId } = appCoverSlice.actions;
  const { profileIsShown, profileId } = useAppSelector((state) => state.appCoverReducer);

  const {
    data: profile,
    isFetching,
    error,
    refetch,
  } = useGetProfileByIdGetQuery(profileId, { skip: profileId === '' });

  const closeHandler = () => {
    dispatch(setProfileIsShown(false));
    dispatch(setProfileId(''));
  };

  return (
    <ModalPage isOpen={profileIsShown} onClose={closeHandler}>
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
