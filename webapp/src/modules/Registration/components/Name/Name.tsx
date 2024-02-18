import { useEffect, useState } from 'react';
import WebApp from '@twa-dev/sdk';
import styles from '../../styles/_common.module.scss';
import { BaseInput } from '../../../../UI';
import { useAppDispatch, useAppSelector } from '../../../../utils/hooks/useRedux';
import { registrationSlice } from '../../store/slice';

export const Name = () => {
  const dispatch = useAppDispatch();
  const { setFormData, setHasErrors } = registrationSlice.actions;
  const {
    formData: { name },
  } = useAppSelector((state) => state.registrationReducer);
  const [hasError, setError] = useState(false);

  const handlerChangeName = (text: string) => {
    const currentHasError = !/^[a-zа-яё\s]+$/i.test(text);
    dispatch(setFormData({ name: text }));
    dispatch(setHasErrors({ name: currentHasError }));
    setError(currentHasError);
  };

  useEffect(() => {
    const tgName = WebApp.initDataUnsafe.user?.first_name;
    if (tgName) {
      handlerChangeName(tgName);
    }
  }, []);

  return (
    <div className={styles.block}>
      <div className={styles.title}>Ваше имя</div>
      <BaseInput
        hint="Так оно будет отображаться в приложении"
        value={name}
        onChange={(e) => handlerChangeName(e.target.value)}
        hasError={hasError}
      />
    </div>
  );
};
