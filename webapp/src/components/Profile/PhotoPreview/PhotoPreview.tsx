import { MouseEvent, useMemo, useState } from 'react';
import cn from 'classnames';
import styles from './PhotoPreview.module.scss';
import Avatar from '../../../assets/image/avatar.svg';
import { ReactComponent as MoreIcon } from '../../../assets/icons/more.svg';
import { PhotoI } from '../../../utils/interfaces';
import { DropdownMenu } from '../../DropdownMenu/DropdownMenu';
import { Dropdown, Snackbar } from '../../../UI';
import { getProfileDropdownConfig } from '../utils/config';

interface PhotoPreviewProps {
  photoList: PhotoI[];
  profileId: string;
}

export const PhotoPreview = ({ photoList, profileId }: PhotoPreviewProps) => {
  const [currentPhoto, setCurrentPhoto] = useState(photoList[0]);
  const [hasError, setHasError] = useState(false);
  const [successText, setSuccessText] = useState('');

  const stepLineIsShown = photoList.length > 1;

  const setNextPhotoHandler = (e: MouseEvent<HTMLDivElement>) => {
    if (!stepLineIsShown) {
      return;
    }

    let nextPhoto: PhotoI | undefined;

    if (e.pageX > window.innerWidth / 2) {
      if (photoList.length === currentPhoto.displaying_order) {
        setCurrentPhoto(photoList[0]);
        return;
      }

      nextPhoto = photoList.find((photo) => {
        return photo.displaying_order === currentPhoto.displaying_order + 1;
      });
    } else if (e.pageX < window.innerWidth / 2) {
      if (currentPhoto.displaying_order === 1) {
        setCurrentPhoto(photoList[photoList.length - 1]);
        return;
      }

      nextPhoto = photoList.find((photo) => {
        return photo.displaying_order === currentPhoto.displaying_order - 1;
      });
    }

    if (nextPhoto) {
      setCurrentPhoto(nextPhoto);
    }
  };

  const getAvatar = useMemo(() => {
    if (currentPhoto) {
      return `https://cdn.lovolab.ru/${currentPhoto.url}`;
    }

    return Avatar;
  }, [currentPhoto]);

  const share = () => {
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
  };

  const config = getProfileDropdownConfig(share);

  return (
    <div className={styles.photoPreviewContainer}>
      <img key={getAvatar} src={getAvatar} alt="mainPhoto" onClick={setNextPhotoHandler} role="presentation" />
      <div className={styles.topMenuWrapper}>
        <div className={styles.stepLineWrapper}>
          {stepLineIsShown &&
            photoList.map((photo, index) => (
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
      <Snackbar
        type={hasError ? 'error' : 'success'}
        shouldRender={hasError || !!successText}
        description={successText || 'Ошибка при попытке поделиться профилем'}
      />
    </div>
  );
};
