import WebApp from '@twa-dev/sdk';
import { useNavigate } from 'react-router-dom';
import { useEffect } from 'react';
import { useAppSelector } from '../../../../utils/hooks/useRedux';
import styles from './RegistrationModule.module.scss';
import { CustomButton, Snackbar, TelegramButton } from '../../../../UI';

import { Birthday } from '../Birthday/Birthday';
import { GenderComponent } from '../Gender/Gender';
import { Name } from '../Name/Name';
import { useRegisterProfileProfilePostMutation } from '../../../../redux/api/cheerApi';

export const RegistrationModule = () => {
  const navigate = useNavigate();

  const {
    hasErrors,
    formData: { name, gender, month, day, year },
  } = useAppSelector((state) => state.registrationReducer);
  const [registerProfile, { isLoading: isLoadingRegistry, error: registryError, isSuccess }] =
    useRegisterProfileProfilePostMutation();

  useEffect(() => {
    if (isSuccess) {
      navigate('/feed');
    }
  }, [isSuccess]);

  const onSubmit = () => {
    const requestData = { name, gender, birthdate: `${year}-${month}-${day}` };
    registerProfile(requestData);
  };

  const isDisabled = hasErrors.day || hasErrors.month || hasErrors.year || hasErrors.name || hasErrors.gender;

  return (
    <div className={styles.registrationContainer}>
      <div className={styles.pageTitle}>Создать аккаунт</div>
      <GenderComponent />
      <Name />
      <Birthday />
      <Snackbar shouldRender={!!registryError} description={registryError} />
      {WebApp.platform === 'unknown' ? (
        <div className={styles.buttonWrapper}>
          <CustomButton text="ПРОДОЛЖИТЬ" onClick={onSubmit} isDisabled={isDisabled} isLoading={isLoadingRegistry} />
        </div>
      ) : (
        <TelegramButton text="ПРОДОЛЖИТЬ" onClick={onSubmit} isDisabled={isDisabled} isLoading={isLoadingRegistry} />
      )}
    </div>
  );
};
