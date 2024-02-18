import { DropdownConfigT } from '../../../utils/interfaces/dropdown';
import { ReactComponent as ExportIcon } from '../../../assets/icons/export.svg';

export const getProfileDropdownConfig = (share: VoidFunction): DropdownConfigT => [
  { Icon: ExportIcon, text: 'Поделиться', onClick: share },
];
