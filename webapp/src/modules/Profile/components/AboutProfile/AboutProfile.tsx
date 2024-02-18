import { useEffect } from 'react';
import cn from 'classnames';
import styles from './AboutProfile.module.scss';
import { useAppDispatch, useAppSelector } from '../../../../utils/hooks/useRedux';
import { profilePageSlice } from '../../store/slice';

interface AboutProfileProps {
  info: string | null;
}

export const AboutProfile = ({ info }: AboutProfileProps) => {
  const { bio } = useAppSelector((state) => state.profilePageReducer);
  const { setBio, setCanUpdateBio } = profilePageSlice.actions;
  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(setBio(info ?? ''));
  }, []);

  useEffect(() => {
    let canUpdate = false;

    if (info === null && bio.length === 0) {
      canUpdate = false;
    } else {
      canUpdate = info !== bio;
    }

    dispatch(setCanUpdateBio(canUpdate));
  }, [bio, info]);

  return (
    <div className={styles.aboutProfileContainer}>
      <div className={styles.block}>
        <div className={cn(styles.title, styles.withCounter)}>
          Обо мне
          <div className={styles.counter}>{`(${bio.length}/600)`}</div>
        </div>
        <div>
          <textarea
            className={styles.bioTextArea}
            maxLength={600}
            placeholder="Введите описание профиля"
            value={bio}
            onChange={(event) => dispatch(setBio(event.target.value))}
          />
        </div>
      </div>
    </div>
  );
};
