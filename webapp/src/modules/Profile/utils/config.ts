import { DropdownConfigT } from '../../../utils/interfaces/dropdown';
import { ReactComponent as ExportIcon } from '../../../assets/icons/export.svg';
import { ReactComponent as CameraIcon } from '../../../assets/icons/camera.svg';
import { ReactComponent as UserIcon } from '../../../assets/icons/user.svg';
import { ReactComponent as TrashIcon } from '../../../assets/icons/trash.svg';

interface ProfileDropdownI {
  share: VoidFunction;
  deletePhoto: VoidFunction;
  upload: VoidFunction;
  setMainPhoto: VoidFunction;
}

interface ProfileDropdownDisabledI {
  deletePhotoIsDisabled: boolean;
  uploadIsDisabled: boolean;
  setMainPhotoIsDisabled: boolean;
}

export const getProfileDropdownConfig = (
  { share, deletePhoto, upload, setMainPhoto }: ProfileDropdownI,
  { deletePhotoIsDisabled, uploadIsDisabled, setMainPhotoIsDisabled }: ProfileDropdownDisabledI,
): DropdownConfigT => [
  { Icon: TrashIcon, text: 'Удалить', onClick: deletePhoto, isDisabled: deletePhotoIsDisabled },
  { Icon: CameraIcon, text: 'Загрузить', onClick: upload, isDisabled: uploadIsDisabled },
  { Icon: UserIcon, text: 'Сделать основной', onClick: setMainPhoto, isDisabled: setMainPhotoIsDisabled },
  { Icon: ExportIcon, text: 'Поделиться профилем', onClick: share, isDisabled: false },
];
