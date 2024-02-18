import { ChangeEvent, useEffect, useRef } from 'react';
import styles from './HelperModule.module.scss';
import { Button, Snackbar, UploadAction } from '../../../../UI';
import { ReactComponent as LocationIcon } from '../../../../assets/icons/location.svg';
import { ReactComponent as CameraIcon } from '../../../../assets/icons/camera.svg';
import {
  useGetDeckPostQuery,
  useGetMyProfileProfileGetQuery,
  useUpdateProfilePatchMutation,
  useUploadProfilePhotoPostMutation,
} from '../../../../redux/api/cheerApi';
import { useGeolocation } from '../../utils/useGeolocation';
import { loadPhoto } from '../../../../utils/handlers/loadPhoto';

interface EmptyFeedProps {
  distanceIsEmpty?: boolean;
  photosIsEmpty?: boolean;
}

export const EmptyProfile = ({ distanceIsEmpty, photosIsEmpty }: EmptyFeedProps) => {
  const { refetch: refetchProfile } = useGetMyProfileProfileGetQuery();
  const { refetch: refetchDeck } = useGetDeckPostQuery();
  const [updateGEO, { isSuccess: updateGeoIsSuccess }] = useUpdateProfilePatchMutation();
  const [uploadPhoto, { isLoading: uploadPhotoIsLoading, error: uploadPhotoError, isSuccess: photoLoadIsSuccess }] =
    useUploadProfilePhotoPostMutation();
  const uploadButtonRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (updateGeoIsSuccess) {
      refetchDeck();
    }
  }, [updateGeoIsSuccess]);

  useEffect(() => {
    if (photoLoadIsSuccess) {
      refetchProfile();
    }
  }, [photoLoadIsSuccess]);

  const {
    location,
    isLoading: isLoadingGeo,
    error: errorGeo,
    update: updateGeo,
    isSuccess: isSuccessGeo,
  } = useGeolocation();

  useEffect(() => {
    if (distanceIsEmpty) {
      updateGeo();
    }
  }, []);

  useEffect(() => {
    if (isSuccessGeo && location) {
      updateGEO({ location });
    }
  }, [isSuccessGeo, location]);

  const addFileHandler = (e: ChangeEvent<HTMLInputElement>) => {
    const photo = loadPhoto(e, false);

    if (photo) {
      uploadPhoto(photo);
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.label}>
        Поделитесь своей геопозицией и загрузите свое первое фото, для того чтобы начать
      </div>
      <div className={styles.buttonWrapper}>
        <Button
          text={distanceIsEmpty && !updateGeoIsSuccess ? 'Поделиться' : 'Готово'}
          type={distanceIsEmpty && !updateGeoIsSuccess ? 'default' : 'accept'}
          onClick={updateGeo}
          icon={<LocationIcon />}
          isDisabled={isLoadingGeo || !distanceIsEmpty || updateGeoIsSuccess}
          className={styles.customButton}
        />
        <Button
          text={photosIsEmpty && !photoLoadIsSuccess ? 'Загрузить' : 'Готово'}
          type={photosIsEmpty && !photoLoadIsSuccess ? 'default' : 'accept'}
          isDisabled={uploadPhotoIsLoading || !photosIsEmpty || photoLoadIsSuccess}
          onClick={() => uploadButtonRef.current?.click()}
          icon={<CameraIcon />}
          className={styles.customButton}
        >
          <UploadAction onClick={addFileHandler} ref={uploadButtonRef} />
        </Button>
      </div>
      <Snackbar shouldRender={!!errorGeo} description={errorGeo} />
      <Snackbar shouldRender={!!uploadPhotoError} description={uploadPhotoError} />
    </div>
  );
};
