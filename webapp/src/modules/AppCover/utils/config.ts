import { ReactComponent as NotificationIcon } from '../../../assets/icons/notification.svg';
import { ReactComponent as MoonIcon } from '../../../assets/icons/moon.svg';
import { ReactComponent as ArchiveBookIcon } from '../../../assets/icons/archive-book.svg';
import { ReactComponent as MessageQuestionsIcon } from '../../../assets/icons/message-question.svg';
import { ReactComponent as MoneyIcon } from '../../../assets/icons/money-recive.svg';
import { ReactComponent as UserRemove } from '../../../assets/icons/user-remove.svg';
import { ReactComponent as PathIcon } from '../../../assets/icons/path.svg';
import { ReactComponent as MessageIcon } from '../../../assets/icons/message-2.svg';
import { ReactComponent as HeartIcon } from '../../../assets/icons/heart.svg';
import { ReactComponent as ProfileIcon } from '../../../assets/icons/profile.svg';
import { ReactComponent as NoteIcon } from '../../../assets/icons/note.svg';
import { SettingItems } from './constants';
import { PagesLink } from '../../../utils/constants';

export const settingsConfig = [
  {
    blockName: 'Общие настройки',
    blockItems: [
      {
        Icon: NotificationIcon,
        name: 'Уведомления',
        action: SettingItems.notification,
      },
      {
        Icon: MoonIcon,
        name: 'Тема оформления',
        action: SettingItems.theme,
      },
      {
        Icon: UserRemove,
        name: 'Удаление профиля',
        action: SettingItems.deleteProfile,
      },
    ],
  },
  {
    blockName: 'Помощь',
    blockItems: [
      {
        Icon: PathIcon,
        name: 'Написать разработчикам',
        action: SettingItems.openChat,
      },
      {
        Icon: MessageQuestionsIcon,
        name: 'Ф.А.КЮ',
        action: SettingItems.faq,
      },
      {
        Icon: MoneyIcon,
        name: 'Отдать свои деньги',
        action: SettingItems.empty,
      },
      {
        Icon: ArchiveBookIcon,
        name: 'Политика конфиденциальности',
        action: SettingItems.empty,
      },
    ],
  },
];

export const bottomNavigationConfig = [
  {
    Icon: NoteIcon,
    page: PagesLink.feed,
  },
  {
    Icon: MessageIcon,
    page: PagesLink.matches,
  },
  {
    Icon: HeartIcon,
    page: PagesLink.interaction,
  },
  {
    Icon: ProfileIcon,
    page: PagesLink.profile,
  },
];
