import { ChangeEvent, MouseEvent, useCallback, useEffect, useMemo, useRef, useState } from 'react';
import cn from 'classnames';
import WebApp from '@twa-dev/sdk';
import styles from './PhotoPreview.module.scss';
import { PhotoI } from '../../../../utils/interfaces';
import Avatar from '../../../../assets/image/avatar.svg';
import { ReactComponent as CameraIcon } from '../../../../assets/icons/camera.svg';
import { ReactComponent as UserIcon } from '../../../../assets/icons/user.svg';
import { ReactComponent as TrashIcon } from '../../../../assets/icons/trash.svg';
import { ReactComponent as MoreIcon } from '../../../../assets/icons/more.svg';
import { loadPhoto } from '../../../../utils/handlers/loadPhoto';
import { Dropdown, Snackbar, UploadAction } from '../../../../UI';
import { useAppDispatch, useAppSelector } from '../../../../utils/hooks/useRedux';
import { profilePageSlice } from '../../store/slice';
import { LocalPhotoI } from '../../utils/interfaces';
import { generateLocalPhoto } from '../../utils/generateLocalPhoto';
import { generateId } from '../../../../utils/handlers/generateId';
import { DropdownMenu } from '../../../../components/DropdownMenu/DropdownMenu';
import { getProfileDropdownConfig } from '../../utils/config';

interface PhotoPreviewProps {
  photoList: PhotoI[];
  profileId: string;
}

export const PhotoPreview = ({ photoList, profileId }: PhotoPreviewProps) => {
  const dispatch = useAppDispatch();
  const { removePhoto, setCanUpdatePhoto, addPhoto, setFirstPhoto, setCurrentPhoto } = profilePageSlice.actions;
  const { photoList: customPhotoList, currentPhoto } = useAppSelector((state) => state.profilePageReducer);
  const [hasError, setHasError] = useState(false);
  const [successText, setSuccessText] = useState('');
  const [photoNotification, setPhotoNotification] = useState(false);

  const uploadButtonRef = useRef<HTMLInputElement>(null);
  const stepLineIsShown = currentPhoto && customPhotoList.length > 1;

  useEffect(() => {
    photoList.map((photo) => dispatch(addPhoto(photo)));
    dispatch(setCurrentPhoto(photoList[0] || null));
  }, []);

  useEffect(() => {
    let canUpdate = false;

    if (photoList.length !== customPhotoList.length) {
      canUpdate = true;
    } else if (customPhotoList.length !== 0) {
      canUpdate = !customPhotoList.every((customPhoto, index) => customPhoto.id === photoList[index].id);
    }

    dispatch(setCanUpdatePhoto(canUpdate));
  }, [customPhotoList, photoList]);

  const addFileHandler = useCallback(
    async (e: ChangeEvent<HTMLInputElement>) => {
      if (customPhotoList.length > 4) {
        return;
      }

      const photo = loadPhoto(e, true);

      if (photo) {
        const photoUrl = await generateLocalPhoto(photo);
        const photoData: LocalPhotoI = {
          id: generateId(),
          displaying_order: customPhotoList.length + 1,
          url: photoUrl,
          isLocal: true,
        };
        dispatch(addPhoto(photoData));
        dispatch(setCurrentPhoto(photoData));
      }
    },
    [customPhotoList],
  );

  const setNextPhotoHandler = (e: MouseEvent<HTMLDivElement>) => {
    if (!stepLineIsShown) {
      return;
    }

    let nextPhoto: PhotoI | undefined;

    if (e.pageX > window.innerWidth / 2) {
      if (customPhotoList.length === currentPhoto.displaying_order) {
        dispatch(setCurrentPhoto(customPhotoList[0]));
        return;
      }

      nextPhoto = customPhotoList.find((photo) => {
        return photo.displaying_order === currentPhoto.displaying_order + 1;
      });
    } else if (e.pageX < window.innerWidth / 2) {
      if (currentPhoto.displaying_order === 1) {
        dispatch(setCurrentPhoto(customPhotoList[customPhotoList.length - 1]));
        return;
      }

      nextPhoto = customPhotoList.find((photo) => {
        return photo.displaying_order === currentPhoto.displaying_order - 1;
      });
    }

    if (nextPhoto) {
      dispatch(setCurrentPhoto(nextPhoto));
    }
  };

  const getAvatar = useMemo(() => {
    if (currentPhoto?.isLocal) {
      return currentPhoto.url;
    }

    if (currentPhoto) {
      return `https://cdn.lovolab.ru/${currentPhoto.url}`;
    }

    return Avatar;
  }, [currentPhoto]);

  const deletePhotoHandler = useCallback(() => {
    if (!currentPhoto || customPhotoList.length < 2) return;

    const deleteText = 'Удалить фото?';

    const deletePhoto = (state: boolean) => {
      if (state) {
        dispatch(removePhoto(currentPhoto));
      }
    };

    if (WebApp.platform === 'unknown') {
      // eslint-disable-next-line no-restricted-globals
      const state = confirm(deleteText);
      deletePhoto(state);
    } else {
      WebApp.showConfirm(deleteText, deletePhoto);
    }
  }, [currentPhoto, customPhotoList]);

  const setFirstPhotoHandler = useCallback(() => {
    if (currentPhoto && customPhotoList.length > 1 && currentPhoto.displaying_order !== 1) {
      dispatch(setFirstPhoto(currentPhoto.displaying_order));
      setPhotoNotification(true);
    }
  }, [currentPhoto, customPhotoList]);

  const shareProfile = useCallback(() => {
    setSuccessText('');
    setHasError(false);

    if (navigator.share) {
      navigator
        .share({
          title: 'Профиль на FlirteX',
          url: `https://t.me/flirtexBot/app?startapp=${profileId}-idp`,
        })
        .then(() => setSuccessText('Вы успешно поделились профилем!'))
        .catch(() => setHasError(true));
    } else {
      navigator.clipboard
        .writeText(`https://t.me/flirtexBot/app?startapp=${profileId}-idp`)
        .then(() => setSuccessText('Ссылка на профиль скопирована!'))
        .catch(() => setHasError(true));
    }
  }, []);

  const config = getProfileDropdownConfig(
    {
      share: shareProfile,
      setMainPhoto: setFirstPhotoHandler,
      upload: () => uploadButtonRef.current?.click(),
      deletePhoto: deletePhotoHandler,
    },
    {
      setMainPhotoIsDisabled: !currentPhoto || currentPhoto?.displaying_order === 1,
      uploadIsDisabled: customPhotoList.length > 4,
      deletePhotoIsDisabled: !stepLineIsShown,
    },
  );

  return (
    <div className={styles.photoPreviewContainer}>
      <img key={getAvatar} src={getAvatar} alt="mainPhoto" onClick={setNextPhotoHandler} role="presentation" />
      <div className={styles.topMenuWrapper}>
        <div className={styles.stepLineWrapper}>
          {stepLineIsShown &&
            customPhotoList.map((photo, index) => (
              <div
                key={photo.id}
                className={cn(styles.stepLine, { [styles.active]: currentPhoto.displaying_order === index + 1 })}
              />
            ))}
        </div>
        <Dropdown
          className={styles.optionWrapper}
          buttonClassName={styles.buttonWrapper}
          canClose
          placement="auto-start"
        >
          <MoreIcon />
          <DropdownMenu config={config} />
        </Dropdown>
      </div>
      <div className={styles.bottomMenuWrapper}>
        <div className={styles.actionWrapper}>
          <div
            className={cn(styles.actionButton, {
              [styles.disable]: !stepLineIsShown,
            })}
            onClick={deletePhotoHandler}
            role="presentation"
          >
            <TrashIcon />
          </div>
          <div
            className={cn(styles.actionButton, styles.addPhotoButton, {
              [styles.disable]: customPhotoList.length > 4,
            })}
            onClick={() => uploadButtonRef.current?.click()}
            role="presentation"
          >
            <CameraIcon />
            <UploadAction onClick={addFileHandler} ref={uploadButtonRef} />
          </div>
          <div
            className={cn(styles.actionButton, {
              [styles.disable]: !currentPhoto || currentPhoto?.displaying_order === 1,
            })}
            onClick={setFirstPhotoHandler}
            role="presentation"
          >
            <UserIcon />
          </div>
        </div>
      </div>
      <Snackbar
        type={hasError ? 'error' : 'success'}
        shouldRender={hasError || !!successText}
        description={successText || 'Ошибка при попытке поделиться профилем'}
      />
      <Snackbar
        type="success"
        shouldRender={photoNotification}
        description="Фотография установлена как основная"
        onClose={() => setPhotoNotification(false)}
      />
    </div>
  );
};
