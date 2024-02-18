import WebApp from '@twa-dev/sdk';
import { useEffect, useState } from 'react';
import styles from './ProfileModule.module.scss';
import { PhotoPreview } from '../PhotoPreview/PhotoPreview';
import { AboutProfile } from '../AboutProfile/AboutProfile';
import { Interests } from '../Interests/Interests';
import {
  useEditPhotoOrderInProfilePatchMutation,
  useGetMyProfileProfileGetQuery,
  useRemovePhotoFromProfileDeleteMutation,
  useUpdateProfilePatchMutation,
  useUploadProfilePhotoPostMutation,
} from '../../../../redux/api/cheerApi';
import { CustomButton, Snackbar, TelegramButton } from '../../../../UI';
import { useAppDispatch, useAppSelector } from '../../../../utils/hooks/useRedux';
import { profilePageSlice } from '../../store/slice';
import { CustomErrorI } from '../../../../utils/interfaces';
import { Name } from '../Name/Name';
import { ErrorComponent } from '../../../../components/ErrorComponent/ErrorComponent';
import { ProfileSkeleton } from '../ProfileSkeleton/ProfileSkeleton';

export const ProfileModule = () => {
  const {
    data: profile,
    isLoading: profileIsLoading,
    error: profileError,
    refetch: profileRefetch,
  } = useGetMyProfileProfileGetQuery();
  const [updateProfile] = useUpdateProfilePatchMutation();
  const [uploadPhoto] = useUploadProfilePhotoPostMutation();
  const [fetchDeletePhoto] = useRemovePhotoFromProfileDeleteMutation();
  const [editPhotoOrder] = useEditPhotoOrderInProfilePatchMutation();

  const dispatch = useAppDispatch();
  const { reset, updateLocalPhoto } = profilePageSlice.actions;
  const { bio, photoList, interests, photoCanUpdate, interestsCanUpdate, bioCanUpdate, removedPhotoIdList } =
    useAppSelector((state) => state.profilePageReducer);

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<CustomErrorI | null>(null);
  const [isSuccess, setIsSuccess] = useState(false);
  const isDisabled = !bioCanUpdate && !interestsCanUpdate && !photoCanUpdate;

  useEffect(() => {
    return () => {
      dispatch(reset());
    };
  }, []);

  useEffect(() => {
    if (!isDisabled) {
      WebApp.MainButton.show();
    } else {
      WebApp.MainButton.hide();
    }
  }, [isDisabled]);

  const submitHandler = async () => {
    try {
      setError(null);
      setIsLoading(true);
      setIsSuccess(false);

      let newIdList: string[] = [];
      let canUpdateOrder = false;
      const interestsId = interests.map(({ id }) => id);
      const newPhoto = photoList.filter(({ isLocal }) => isLocal);

      if (removedPhotoIdList.length) {
        const removedPhotoIdListPromises = removedPhotoIdList.map((photoId) => fetchDeletePhoto(photoId).unwrap());
        await Promise.all(removedPhotoIdListPromises);
      }

      if (newPhoto.length) {
        const photoLinksPromises = newPhoto.map(({ url }) => fetch(url));
        const photoLinksResponse = await Promise.all(photoLinksPromises);
        const blobPromises = photoLinksResponse.map((photo) => photo.blob());
        const blobs = await Promise.all(blobPromises);
        const photoPromises = blobs.map((blob) => {
          const file = new File([blob], 'userPhoto');
          const photoForm = new FormData();
          photoForm.append('photo', file);
          return uploadPhoto(photoForm).unwrap();
        });
        const photoResponse = await Promise.all(photoPromises);
        newIdList = photoResponse.map(({ id }) => id);
        dispatch(updateLocalPhoto(photoResponse));
      }

      const orderList = photoList.map((photo, index) => {
        let photoId = photo.id;

        if (profile?.photos[index]?.id !== photo.id) {
          canUpdateOrder = true;
        }

        if (photo.isLocal) {
          photoId = newIdList.shift() ?? photo.id;
        }

        return { photo_id: photoId, displaying_order: photo.displaying_order };
      });

      if (canUpdateOrder) {
        await editPhotoOrder(orderList).unwrap();
      }

      if (bioCanUpdate || interestsCanUpdate) {
        await updateProfile({ bio, interests: interestsId }).unwrap();
      } else if (photoCanUpdate) {
        await profileRefetch();
      }

      setIsSuccess(true);
    } catch (e) {
      setError(e as CustomErrorI);
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  if (profileIsLoading) {
    return <ProfileSkeleton />;
  }

  if (!profile || profileError) {
    return <ErrorComponent onClick={profileRefetch} />;
  }

  return (
    <div className={styles.profileContainer}>
      <PhotoPreview photoList={profile.photos} profileId={profile.id} />
      <Name name={profile.name} age={profile.age} gender={profile.gender} />
      <AboutProfile info={profile.bio} />
      <Interests defaultInterests={profile.interests} />
      {WebApp.platform === 'unknown' ? (
        <div className={styles.buttonWrapper}>
          <CustomButton
            text="Сохранить"
            onClick={submitHandler}
            isDisabled={isDisabled || isLoading}
            isLoading={isLoading}
          />
        </div>
      ) : (
        <TelegramButton
          text="Сохранить"
          onClick={submitHandler}
          isDisabled={isDisabled || isLoading}
          isLoading={isLoading}
        />
      )}
      <div>
        <div className={styles.space} />
      </div>
      <Snackbar shouldRender={!!error} description={error ?? ''} />
      <Snackbar shouldRender={isSuccess} type="success" description="Профиль успешно обновлен" />
    </div>
  );
};
