import { memo, MouseEvent } from 'react';
import WebApp from '@twa-dev/sdk';
import styles from './ChatLine.module.scss';
import { DropdownChat } from '../DropdownChat/DropdownChat';
import { MatchesProfileI } from '../../../../utils/interfaces/response/matches';
import Avatar from '../../../../assets/image/avatar.svg';
import { useAppDispatch } from '../../../../utils/hooks/useRedux';
import { matchesSlice } from '../../store/slice';

interface ChatLineProps {
  profile: MatchesProfileI;
}

export const ChatLine = memo(({ profile }: ChatLineProps) => {
  const dispatch = useAppDispatch();
  const { setIsShownModal, setProfileId } = matchesSlice.actions;

  const openProfileHandler = (e: MouseEvent<HTMLDivElement>) => {
    e.stopPropagation();
    dispatch(setProfileId(profile.profile_id));
    dispatch(setIsShownModal(true));
  };

  const writeMessage = (userLink: string) => () => {
    if (userLink.length) {
      WebApp.openTelegramLink(`https://t.me/${userLink}`);
    }
  };

  const getAvatar = () => {
    if (profile.photo_url) {
      return `https://cdn.lovolab.ru/${profile.photo_url}`;
    }

    return Avatar;
  };

  return (
    <div
      key={profile.profile_id}
      className={styles.chatLine}
      onClick={writeMessage(profile.tg_username)}
      role="presentation"
    >
      <div className={styles.imageWrapper} onClick={openProfileHandler} role="presentation">
        <img src={getAvatar()} alt="profile" />
      </div>
      <div className={styles.information}>
        <div className={styles.nameWrapper}>
          <div className={styles.name}>{profile.name}</div>
          <div className={styles.description}>{profile.bio}</div>
        </div>
        <DropdownChat profileId={profile.profile_id} userLink={profile.tg_username} />
      </div>
    </div>
  );
});
