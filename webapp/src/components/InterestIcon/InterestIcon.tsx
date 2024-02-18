import { InterestsIcons } from '../../utils/constants';

interface InterestsIconsProps {
  iconId: string;
}

export const InterestIcon = ({ iconId }: InterestsIconsProps) => {
  const CurrentIcon = InterestsIcons[iconId];

  return <CurrentIcon />;
};
