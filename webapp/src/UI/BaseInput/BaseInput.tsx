import cn from 'classnames';
import { forwardRef, ForwardRefRenderFunction, InputHTMLAttributes } from 'react';
import styles from './BaseInput.module.scss';

interface BaseInputProps extends InputHTMLAttributes<HTMLInputElement> {
  isDisabled?: boolean;
  className?: string;
  hasError?: boolean;
  errorText?: boolean;
  hint?: string;
  label?: string;
}

const BaseInputRef: ForwardRefRenderFunction<HTMLInputElement, BaseInputProps> = (
  { hint, label, hasError, errorText, isDisabled, className, ...attributes },
  ref,
) => {
  return (
    <div className={cn(className, styles.inputContainer)}>
      <div className={cn(styles.inputUnderlined, { [styles.inputDanger]: hasError })}>
        <input required disabled={isDisabled} {...attributes} ref={ref} />
        {label && <span className={styles.inputLabel}>{label}</span>}
        {hasError && errorText && <span className={styles.inputHelper}>{errorText}</span>}
        {hint && !(hasError && errorText) && <span className={styles.inputHelper}>{hint}</span>}
      </div>
    </div>
  );
};

export const BaseInput = forwardRef<HTMLInputElement, BaseInputProps>(BaseInputRef);
