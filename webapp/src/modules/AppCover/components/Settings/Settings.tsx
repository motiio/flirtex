import { SettingItems } from '../../utils/constants';
import styles from './Settings.module.scss';
import { settingsConfig } from '../../utils/config';
import packageJson from '../../../../../package.json';
import { ReactComponent as ArrowRightIcon } from '../../../../assets/icons/arrow-right-line.svg';
import { useAppDispatch } from '../../../../utils/hooks/useRedux';
import { appCoverSlice } from '../../store/slice';

export const Settings = () => {
  const dispatch = useAppDispatch();
  const { setSettingItem } = appCoverSlice.actions;

  const clickItemHandler = (name: SettingItems) => {
    dispatch(setSettingItem(name));
  };

  return (
    <div className={styles.settingContainer}>
      {settingsConfig.map((block) => (
        <div key={block.blockName} className={styles.block}>
          <div className={styles.title}>{block.blockName}</div>
          <div className={styles.blockItems}>
            {block.blockItems.map(({ name, Icon, action }) => (
              <div key={name} className={styles.item} onClick={() => clickItemHandler(action)} role="presentation">
                <div className={styles.itemIcon}>
                  <Icon />
                </div>
                <div className={styles.itemName}>
                  {name}
                  <div className={styles.arrowRight}>
                    <ArrowRightIcon />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
      <div className={styles.company}>
        FlirteX: &nbsp;
        {packageJson.version}
      </div>
    </div>
  );
};
