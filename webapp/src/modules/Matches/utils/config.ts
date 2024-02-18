import { ReactComponent as UserIcon } from '../../../assets/icons/user.svg';
import { ReactComponent as EditIcon } from '../../../assets/icons/edit-2.svg';
import { DropdownConfigT } from '../../../utils/interfaces/dropdown';

export const getDropdownConfig = (openProfile: VoidFunction, writeMessage: VoidFunction): DropdownConfigT => [
  { Icon: UserIcon, text: 'Открыть профиль', onClick: openProfile },
  { Icon: EditIcon, text: 'Перейти в чат', onClick: writeMessage },
];
