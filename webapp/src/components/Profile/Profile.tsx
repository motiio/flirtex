import { ProfileResponseI } from '../../utils/interfaces';
import { PhotoPreview } from './PhotoPreview/PhotoPreview';
import { Name } from './Name/Name';
import { AboutProfile } from './AboutProfile/AboutProfile';
import { Interests } from './Interests/Interests';

interface ProfileProps {
  profile: ProfileResponseI;
}

export const Profile = ({ profile }: ProfileProps) => {
  return (
    <>
      <PhotoPreview photoList={profile.photos} profileId={profile.id} />
      <Name name={profile.name} age={profile.age} gender={profile.gender} distance={profile.distance} />
      <AboutProfile info={profile.bio ?? ''} />
      <Interests interests={profile.interests} />
    </>
  );
};
