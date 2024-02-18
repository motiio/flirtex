import { useMemo } from 'react';
import WebApp from '@twa-dev/sdk';
import styles from './DropdownChat.module.scss';
import { Dropdown } from '../../../../UI';
import { getDropdownConfig } from '../../utils/config';
import { ReactComponent as MoreIcon } from '../../../../assets/icons/more.svg';
import { DropdownConfigT } from '../../../../utils/interfaces/dropdown';
import { DropdownMenu } from '../../../../components/DropdownMenu/DropdownMenu';
import { useAppDispatch } from '../../../../utils/hooks/useRedux';
import { matchesSlice } from '../../store/slice';

interface DropdownMenuProps {
  profileId: string;
  userLink: string;
}

export const DropdownChat = ({ profileId, userLink }: DropdownMenuProps) => {
  const dispatch = useAppDispatch();
  const { setIsShownModal, setProfileId } = matchesSlice.actions;

  const config: DropdownConfigT = useMemo(() => {
    const openProfile = () => {
      dispatch(setProfileId(profileId));
      dispatch(setIsShownModal(true));
    };

    const writeMessage = () => {
      if (userLink.length) {
        WebApp.openLink(`https://t.me/${userLink}`);
      }
    };

    return getDropdownConfig(openProfile, writeMessage);
  }, []);

  return (
    <Dropdown canClose placement="auto-start" buttonClassName={styles.option}>
      <MoreIcon />
      <DropdownMenu config={config} />
    </Dropdown>
  );
};
