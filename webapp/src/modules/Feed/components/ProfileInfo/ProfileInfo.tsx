import cn from 'classnames';
import styles from './ProfileInfo.module.scss';
import { Chip } from '../../../../UI';
import { useAppSelector } from '../../../../utils/hooks/useRedux';
import { InterestIcon } from '../../../../components/InterestIcon/InterestIcon';
import { ReactComponent as LocationIcon } from '../../../../assets/icons/location.svg';

export const ProfileInfo = () => {
  const { profilesBatch } = useAppSelector((state) => state.feedReducer);
  const profile = profilesBatch[0];

  if (!profile) {
    return (
      <div className={styles.profileInfoContainer}>
        <div className={styles.errorLabel}>Мы где то потеряли профиль...</div>
      </div>
    );
  }

  return (
    <div className={styles.profileInfoContainer}>
      <div className={styles.block}>
        <div className={cn(styles.blockLabel, styles.info)}>
          <div className={styles.name}>
            {profile.name}
            ,&nbsp;
            {profile.age}
          </div>
          <div className={styles.distance}>
            <LocationIcon />
            &nbsp;&lt;&nbsp;
            {profilesBatch[0].distance}
            &nbsp;км
          </div>
        </div>
      </div>
      {!!profile.interests.length && (
        <div className={styles.block}>
          <div className={styles.blockLabel}>Интересы</div>
          <div className={cn(styles.blockContent, styles.chips)}>
            {profilesBatch[0].interests.map((interest) => (
              <Chip key={interest.id} text={interest.name} icon={<InterestIcon iconId={interest.id} />} />
            ))}
          </div>
        </div>
      )}
      <div className={styles.block}>
        <div className={styles.blockLabel}>О себе</div>
        <div className={styles.blockContent}>{profile.bio ?? 'Описание отсутствует.'}</div>
      </div>
    </div>
  );
};
