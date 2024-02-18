import styles from './Gender.module.scss';
import { Button } from '../../../../UI';
import { Gender } from '../../../../utils/constants';
import { ReactComponent as WomanIcon } from '../../../../assets/icons/woman.svg';
import { ReactComponent as ManIcon } from '../../../../assets/icons/man.svg';
import { useAppDispatch, useAppSelector } from '../../../../utils/hooks/useRedux';
import { registrationSlice } from '../../store/slice';

export const GenderComponent = () => {
  const dispatch = useAppDispatch();
  const { setFormData, setHasErrors } = registrationSlice.actions;
  const {
    formData: { gender },
  } = useAppSelector((state) => state.registrationReducer);

  const changeGenderHandler = (selectedGender: Gender) => {
    if (selectedGender !== gender) {
      dispatch(setFormData({ gender: selectedGender }));
      dispatch(setHasErrors({ gender: false }));
    }
  };

  return (
    <div className={styles.block}>
      <div className={styles.title}>Какой у вас пол?</div>
      <div className={styles.genderWrapper}>
        <Button
          text="Парень"
          type={gender === Gender.male ? 'default' : 'disable'}
          onClick={() => changeGenderHandler(Gender.male)}
          icon={<ManIcon />}
          iconWrapper={false}
          className={styles.customGender}
        />
        <Button
          text="Девушка"
          type={gender === Gender.female ? 'default' : 'disable'}
          onClick={() => changeGenderHandler(Gender.female)}
          icon={<WomanIcon />}
          iconWrapper={false}
          className={styles.customGender}
        />
      </div>
    </div>
  );
};
