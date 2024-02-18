import { useEffect } from 'react';
import cn from 'classnames';
import styles from './Interests.module.scss';
import { InterestI } from '../../../../utils/interfaces';
import { useGetInterestsGetQuery } from '../../../../redux/api/cheerApi';
import { Chip, Snackbar } from '../../../../UI';
import { useAppDispatch, useAppSelector } from '../../../../utils/hooks/useRedux';
import { profilePageSlice } from '../../store/slice';
import { InterestIcon } from '../../../../components/InterestIcon/InterestIcon';
import { InterestsSkeleton } from './Interests.skeleton';

interface InterestsProps {
  defaultInterests: InterestI[];
}

export const Interests = ({ defaultInterests }: InterestsProps) => {
  const {
    data: interestsData,
    error: interestsError,
    isError: interestsIsError,
    isLoading: interestsIsLoading,
  } = useGetInterestsGetQuery();

  const dispatch = useAppDispatch();
  const { interests: selectedInterests } = useAppSelector((state) => state.profilePageReducer);
  const { setInterest, setCanUpdateInterests } = profilePageSlice.actions;

  useEffect(() => {
    defaultInterests.map((interests) => dispatch(setInterest(interests)));
  }, []);

  useEffect(() => {
    let canUpdate = false;

    if (defaultInterests.length === selectedInterests.length) {
      const interestsId = selectedInterests.map((interest) => interest.id);
      canUpdate = !defaultInterests.every((interest) => interestsId.includes(interest.id));
    } else {
      canUpdate = true;
    }

    dispatch(setCanUpdateInterests(canUpdate));
  }, [selectedInterests, defaultInterests]);

  if (!interestsData || interestsIsLoading) {
    return <InterestsSkeleton />;
  }

  return (
    <div className={styles.interestsContainer}>
      <div className={styles.block}>
        <div className={cn(styles.title, styles.withCounter)}>
          Интересы
          <div className={styles.counter}>{`(${selectedInterests.length}/7)`}</div>
        </div>
        <div className={styles.chipsWrapper}>
          {interestsData?.interests.map((interest) => (
            <Chip
              key={interest.id}
              text={interest.name}
              isSelected={selectedInterests.some((item) => item.id === interest.id)}
              onClick={() => dispatch(setInterest(interest))}
              icon={<InterestIcon iconId={interest.id} />}
            />
          ))}
        </div>
      </div>
      <Snackbar shouldRender={interestsIsError} description={interestsError} />
    </div>
  );
};
