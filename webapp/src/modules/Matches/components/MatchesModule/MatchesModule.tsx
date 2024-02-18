import { useEffect } from 'react';
import styles from './MatchesModule.module.scss';
import { ChatLines } from '../ChatLines/ChatLines';
import { Modal } from '../Modal/Modal';
import { useAppDispatch } from '../../../../utils/hooks/useRedux';
import { matchesSlice } from '../../store/slice';

export const MatchesModule = () => {
  const dispatch = useAppDispatch();
  const { reset } = matchesSlice.actions;

  useEffect(() => {
    return () => {
      dispatch(reset());
    };
  }, []);

  return (
    <div className={styles.matchModuleContainer}>
      <div className={styles.titleWrapper}>
        <div className={styles.title}>Совпадения</div>
      </div>
      <ChatLines />
      <Modal />
    </div>
  );
};
