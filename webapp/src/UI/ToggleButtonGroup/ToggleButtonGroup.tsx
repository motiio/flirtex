import cn from 'classnames';
import styles from './ToggleButtonGroup.module.scss';

export interface ToggleButtonGroupProps<T> {
  options: { name: T; text: string }[];
  onChange: (option: T) => void;
  value?: T;
}

export function ToggleButtonGroup<T>({ value, options, onChange }: ToggleButtonGroupProps<T>) {
  const selectHandler = (optionName: T) => {
    if (value !== optionName) {
      onChange(optionName);
    }
  };

  return (
    <div className={styles.toggleContainer}>
      {options.map((option) => (
        <div
          key={String(option.name)}
          className={cn(styles.toggleButton, { [styles.selected]: option.name === value })}
          onClick={() => selectHandler(option.name)}
          role="presentation"
        >
          <div>{option.text}</div>
        </div>
      ))}
    </div>
  );
}
