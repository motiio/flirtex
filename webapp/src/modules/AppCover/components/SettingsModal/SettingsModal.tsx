import { useEffect } from 'react';
import WebApp from '@twa-dev/sdk';
import { ModalPage } from '../../../../components/ModalPage/ModalPage';
import { useAppDispatch, useAppSelector } from '../../../../utils/hooks/useRedux';
import { Settings } from '../Settings/Settings';
import { useLazyDeleteMyProfileQuery, useSetLikePostMutation } from '../../../../redux/api/cheerApi';
import { authSlice } from '../../../../redux/feature/authSlice';
import { appCoverSlice } from '../../store/slice';
import { SettingItems } from '../../utils/constants';

export const SettingsModal = () => {
  const [deleteProfile, { data, isLoading, isError, error }] = useLazyDeleteMyProfileQuery();
  const dispatch = useAppDispatch();
  const { setHasProfile, addTokens } = authSlice.actions;
  const { setSettingItem, setSettingsIsShown } = appCoverSlice.actions;
  const { settingItem, settingsIsShown } = useAppSelector((state) => state.appCoverReducer);
  const [setLike] = useSetLikePostMutation();

  useEffect(() => {
    const settingClick = () => {
      dispatch(setSettingsIsShown(!settingsIsShown));
    };

    WebApp.SettingsButton.show().onClick(settingClick);
  }, [settingsIsShown]);

  useEffect(() => {
    if (settingItem === SettingItems.deleteProfile) {
      const deleteHandler = (state: boolean) => {
        dispatch(setSettingItem(SettingItems.empty));

        if (state) {
          deleteProfile()
            .unwrap()
            .then(() => {
              dispatch(setHasProfile(null));
              dispatch(addTokens({ refresh_token: '', access_token: '' }));
            });
        }
      };

      if (WebApp.platform === 'unknown') {
        // eslint-disable-next-line no-restricted-globals
        const state = confirm('Вы действительно хотите удалить аккаунт?');
        deleteHandler(state);
      } else {
        WebApp.showConfirm('Вы действительно хотите удалить аккаунт?', deleteHandler);
      }
    }

    if (settingItem === SettingItems.openChat) {
      WebApp.openLink('https://t.me/flirtex', { try_instant_view: true });
    }

    if (settingItem === SettingItems.faq) {
      setLike('28a5bbd3-0a7e-432a-8207-7a06c071c61f');
    }
  }, [settingItem]);

  const closeHandler = () => {
    dispatch(setSettingsIsShown(false));
  };

  return (
    <ModalPage isOpen={settingsIsShown} onClose={closeHandler}>
      <Settings />
    </ModalPage>
  );
};
