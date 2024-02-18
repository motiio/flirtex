import { Sidebar } from '../../../../components/Sidebar/Sidebar';
import { Filter } from '../Filter/Filter';
import { useAppDispatch, useAppSelector } from '../../../../utils/hooks/useRedux';
import { feedSlice } from '../../store/slice';

export const FilterSidebar = () => {
  const dispatch = useAppDispatch();
  const { setFilterIsView } = feedSlice.actions;
  const { filterIsView } = useAppSelector((state) => state.feedReducer);

  const outsideClickHandler = () => {
    dispatch(setFilterIsView(false));
  };

  return (
    <Sidebar isOpen={filterIsView} onOutsideClick={outsideClickHandler}>
      <Filter />
    </Sidebar>
  );
};
