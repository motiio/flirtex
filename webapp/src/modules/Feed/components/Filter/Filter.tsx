import { useEffect, useState } from 'react';
import cn from 'classnames';
import WebApp from '@twa-dev/sdk';
import { useAppDispatch } from '../../../../utils/hooks/useRedux';
import { feedSlice } from '../../store/slice';
import styles from './Filter.module.scss';
import { Button, CustomButton, Slider, Snackbar, TelegramButton, ToggleButtonGroup } from '../../../../UI';
import { Gender } from '../../../../utils/constants';
import { ReactComponent as LocationIcon } from '../../../../assets/icons/location.svg';
import {
  useGetFilterGetQuery,
  useUpdateFilterPatchMutation,
  useUpdateProfilePatchMutation,
} from '../../../../redux/api/cheerApi';
import { FilterSkeleton } from './Filter.skeleton';
import { ErrorComponent } from '../../../../components/ErrorComponent/ErrorComponent';
import { useGeolocation } from '../../utils/useGeolocation';
import { filterOptions } from '../../utils/config';

export const Filter = () => {
  const dispatch = useAppDispatch();
  const { setFilterIsView, setCanForceUpdate } = feedSlice.actions;
  const {
    data: initialFilter,
    isLoading: isLoadingFilter,
    error: errorFilter,
    refetch: refetchFilterData,
  } = useGetFilterGetQuery();
  const [updateFilter, { isLoading: isLoadingUpdate }] = useUpdateFilterPatchMutation();
  const [updateGEO, { isLoading: idUpdateGeo }] = useUpdateProfilePatchMutation();

  const [gender, setGender] = useState(Gender.other);
  const [age, setAge] = useState([19, 22]);
  const [distance, setDistance] = useState(5);
  const {
    location,
    isLoading: isLoadingGeo,
    error: errorGeo,
    update: updateGPSHandler,
    isSuccess: isSuccessGeo,
  } = useGeolocation();

  const isLoadingRegistry = isLoadingUpdate || idUpdateGeo;
  const isActiveButton =
    age[0] !== initialFilter?.age_from ||
    age[1] !== initialFilter?.age_to ||
    distance !== initialFilter?.max_distance ||
    gender !== initialFilter?.looking_gender ||
    isSuccessGeo;

  useEffect(() => {
    if (initialFilter) {
      const { age_from, age_to, max_distance, looking_gender } = initialFilter;
      setGender(looking_gender);
      setDistance(max_distance);
      setAge([age_from, age_to]);
    }
  }, [initialFilter]);

  const onSubmit = async () => {
    try {
      await updateFilter({
        age_from: age[0],
        age_to: age[1],
        max_distance: distance,
        looking_gender: gender,
      });

      if (location) {
        await updateGEO({ location });
      }

      dispatch(setFilterIsView(false));
      dispatch(setCanForceUpdate(true));
    } catch (e) {
      console.error(e);
    }
  };

  if (isLoadingFilter) {
    return <FilterSkeleton />;
  }

  if (errorFilter || !initialFilter) {
    return (
      <div className={styles.errorContainer}>
        <ErrorComponent error={errorFilter} onClick={refetchFilterData} />
      </div>
    );
  }

  return (
    <div className={styles.filterContainer}>
      <div className={styles.label}>Фильтр</div>
      <div className={styles.block}>
        <div className={styles.blockTitle}>Я ищу</div>
        <ToggleButtonGroup value={gender} options={filterOptions} onChange={(option) => setGender(option)} />
      </div>
      <div className={styles.block}>
        <div className={styles.blockTitle}>Возраст</div>
        <div className={styles.sliderWrapper}>
          <Slider min={18} max={60} onChange={(value) => setAge(value as number[])} value={age} range pushable={2} />
          <div className={styles.title}>{`${age[0]}-${age[1]}`}</div>
        </div>
      </div>
      <div className={styles.block}>
        <div className={styles.blockTitle}>Расстояние</div>
        <div className={styles.sliderWrapper}>
          <Slider min={5} max={99} onChange={(value) => setDistance(value as number)} value={distance} />
          <div className={styles.title}>{`${distance} км`}</div>
        </div>
      </div>
      <div className={cn(styles.block, styles.geo)}>
        <Button
          text={isSuccessGeo ? 'ОБНОВЛЕНО' : 'ОБНОВИТЬ СВОЮ ГЕОПОЗИЦИЮ'}
          type={isSuccessGeo ? 'accept' : 'outline'}
          onClick={updateGPSHandler}
          isDisabled={isLoadingGeo || !!location}
          icon={<LocationIcon />}
        />
      </div>
      {WebApp.platform === 'unknown' ? (
        <div className={styles.buttonWrapper}>
          <CustomButton
            text="ПРИМЕНИТЬ"
            onClick={onSubmit}
            isDisabled={!isActiveButton}
            isLoading={isLoadingRegistry}
          />
        </div>
      ) : (
        <TelegramButton
          text="ПРИМЕНИТЬ"
          onClick={onSubmit}
          isDisabled={!isActiveButton}
          isLoading={isLoadingRegistry}
        />
      )}
      <Snackbar
        shouldRender={isSuccessGeo}
        type="success"
        description="Новая геопозиция получена. Примените изменения в фильтре."
        hasNavigationBar={false}
      />
      <Snackbar shouldRender={!!errorGeo} description={errorGeo} />
    </div>
  );
};
