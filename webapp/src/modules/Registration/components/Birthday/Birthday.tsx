import { ChangeEvent, useRef, useState } from 'react';
import styles from './Birthday.module.scss';
import { BaseInput } from '../../../../UI';
import { useAppDispatch, useAppSelector } from '../../../../utils/hooks/useRedux';
import { registrationSlice } from '../../store/slice';

const dateMask: { [key: string]: RegExp } = {
  day: /^(0[1-9]|[12][0-9]|3[01])$/,
  month: /^(0[1-9]|1[012])$/,
  year: /^((19|20)\d\d)$/,
};

export const Birthday = () => {
  const dispatch = useAppDispatch();
  const {
    formData: { day, year, month },
  } = useAppSelector((state) => state.registrationReducer);
  const { setFormData, setHasErrors } = registrationSlice.actions;
  const [hasError, setError] = useState({ day: false, month: false, year: false });
  const monthRef = useRef<HTMLInputElement | null>(null);
  const yearRef = useRef<HTMLInputElement | null>(null);

  const setDayHandler = (e: ChangeEvent<HTMLInputElement>) => {
    const isCorrect = dateMask.day.test(e.target.value);
    setError((prev) => ({ ...prev, day: !isCorrect }));
    dispatch(setHasErrors({ day: !isCorrect }));
    dispatch(setFormData({ day: e.target.value }));

    if (e.target.value.length === 2 && monthRef.current && isCorrect) {
      monthRef.current.focus();
    }
  };

  const setMonthHandler = (e: ChangeEvent<HTMLInputElement>) => {
    const isCorrect = dateMask.month.test(e.target.value);
    setError((prev) => ({ ...prev, month: !isCorrect }));
    dispatch(setHasErrors({ month: !isCorrect }));
    dispatch(setFormData({ month: e.target.value }));

    if (e.target.value.length === 2 && yearRef.current && isCorrect) {
      yearRef.current.focus();
    }
  };

  const setYearHandler = (e: ChangeEvent<HTMLInputElement>) => {
    const isCorrect = dateMask.year.test(e.target.value);
    setError((prev) => ({ ...prev, year: !isCorrect }));
    dispatch(setHasErrors({ year: !isCorrect }));
    dispatch(setFormData({ year: e.target.value }));
  };

  return (
    <div className={styles.block}>
      <div className={styles.title}>Дата рождения</div>
      <div className={styles.birthdayWrapper}>
        <BaseInput type="number" onChange={setDayHandler} hasError={hasError.day} value={day} />
        <BaseInput type="number" onChange={setMonthHandler} hasError={hasError.month} value={month} ref={monthRef} />
        <BaseInput type="number" onChange={setYearHandler} hasError={hasError.year} value={year} ref={yearRef} />
      </div>
      <div className={styles.subTitle}>Ваш возраст будет виден всем</div>
    </div>
  );
};
