import { memo } from 'react';
import styles from './Card.module.scss';
import Avatar from '../../../../assets/image/avatar.svg';
import { useAppDispatch } from '../../../../utils/hooks/useRedux';
import { interactionSlice } from '../../store/slice';
import { LikeReactionsProfileI } from '../../../../utils/interfaces';

interface CardProps {
  profile: LikeReactionsProfileI;
}

export const Card = memo(({ profile }: CardProps) => {
  const dispatch = useAppDispatch();
  const { setIsShownModal, setProfileId } = interactionSlice.actions;

  const openProfileHandler = (id: string) => {
    dispatch(setProfileId(id));
    dispatch(setIsShownModal(true));
  };

  const getAvatar = () => {
    if (profile.photos.length) {
      return `https://cdn.lovolab.ru/${profile.photos[0].url}`;
    }

    return Avatar;
  };

  return (
    <div className={styles.cardWrapper} onClick={() => openProfileHandler(profile.id)} role="presentation">
      <div className={styles.imageWrapper}>
        <img src={getAvatar()} alt="profilePhoto" />
      </div>
      <div className={styles.nameWrapper}>
        <div className={styles.name}>
          {profile.name}
          {', '}
          {profile.age}
        </div>
      </div>
    </div>
  );
});
