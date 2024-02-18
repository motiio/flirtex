import { FunctionComponent, MouseEvent } from 'react';

interface DropdownI {
  text: string;
  Icon: FunctionComponent;
  onClick: (e?: MouseEvent<HTMLDivElement>) => void;
  type?: 'default' | 'error';
  isDisabled?: boolean;
}

export type DropdownConfigT = DropdownI[];
