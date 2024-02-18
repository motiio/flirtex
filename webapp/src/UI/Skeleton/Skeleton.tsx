import { CSSProperties, ReactNode } from 'react';
import cn from 'classnames';
import styles from './Skeleton.module.scss';

export interface SkeletonProps {
  height?: string | number;
  width?: string | number;
  borderRadius?: string;
  className?: string;
  children?: ReactNode;
}

export const Skeleton = ({ height, width, borderRadius, children, className }: SkeletonProps) => {
  const cssStyles: CSSProperties = {
    width,
    height,
    borderRadius,
  };

  return (
    <div className={cn(styles.skeletonContainer, className)} style={cssStyles}>
      {children}
    </div>
  );
};
