import cn from 'classnames';
import styles from './Tabs.module.scss';

interface TabsProps<T> {
  config: { name: string; value: T }[];
  selected: T;
  onClick: (tab: T) => void;
}

export function Tabs<T>({ config, onClick, selected }: TabsProps<T>) {
  return (
    <div className={styles.tabsContainer}>
      {config.map(({ name, value }) => (
        <div key={name} className={styles.tab} onClick={() => onClick(value)} role="presentation">
          <div className={styles.titleWrapper}>
            <div className={cn(styles.title, { [styles.selected]: selected === value })}>{name}</div>
            {selected === value && <div className={styles.selectedLine} />}
          </div>
        </div>
      ))}
    </div>
  );
}
