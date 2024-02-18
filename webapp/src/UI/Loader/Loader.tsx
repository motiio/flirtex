import cn from 'classnames';
import styles from './Loader.module.scss';

interface LoaderProps {
  isActive?: boolean;
  size?: 'XS' | 'S' | 'M' | 'L';
  className?: string;
}

export const Loader = ({ isActive = true, size = 'M', className }: LoaderProps) => {
  if (!isActive) {
    return null;
  }

  return (
    <span
      className={cn(
        styles.circularLoader,
        {
          [styles.sizeXS]: size === 'XS',
          [styles.sizeS]: size === 'S',
          [styles.sizeM]: size === 'M',
          [styles.sizeL]: size === 'L',
        },
        className,
      )}
    />
  );
};
