import { ChangeEvent, forwardRef, ForwardRefRenderFunction } from 'react';
import cn from 'classnames';
import styles from './UploadAction.module.scss';

interface UploadButtonProps {
  onClick: (e: ChangeEvent<HTMLInputElement>) => void;
  classNames?: string;
  isDisabled?: boolean;
}

const UploadButtonWithoutRef: ForwardRefRenderFunction<HTMLInputElement, UploadButtonProps> = (
  { onClick, classNames, isDisabled },
  ref,
) => {
  const handleClick = (e: ChangeEvent<HTMLInputElement>) => {
    e.stopPropagation();
    onClick(e);
  };

  return (
    <input
      type="file"
      className={cn(styles.hidden, classNames)}
      onChange={handleClick}
      accept="image/jpeg,image/jpg,.jpeg,.jpg"
      disabled={isDisabled}
      ref={ref}
    />
  );
};

export const UploadAction = forwardRef<HTMLInputElement, UploadButtonProps>(UploadButtonWithoutRef);
