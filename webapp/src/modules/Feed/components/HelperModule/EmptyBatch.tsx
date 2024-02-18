import styles from './HelperModule.module.scss';
import { ReactComponent as FilterIcon } from '../../../../assets/icons/filter.svg';
import { Button } from '../../../../UI';
import { useAppDispatch } from '../../../../utils/hooks/useRedux';
import { feedSlice } from '../../store/slice';

export const EmptyBatch = () => {
  const dispatch = useAppDispatch();
  const { setFilterIsView } = feedSlice.actions;

  const openFilterHandler = () => {
    dispatch(setFilterIsView(true));
  };

  return (
    <div className={styles.container}>
      <div className={styles.label}>
        Подборка закончилась.
        <br />
        Поменяйте фильтр
      </div>
      <div className={styles.buttonWrapper}>
        <Button
          text="Открыть фильтр"
          onClick={openFilterHandler}
          icon={<FilterIcon />}
          className={styles.customButton}
        />
      </div>
    </div>
  );
};
