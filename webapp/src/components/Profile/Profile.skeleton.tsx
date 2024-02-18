import { PhotoPreviewSkeleton } from './PhotoPreview/PhotoPreview.skeleton';
import { NameSkeleton } from './Name/Name.skeleton';
import { AboutProfileSkeleton } from './AboutProfile/AboutProfile.skeleton';
import { InterestsSkeleton } from './Interests/Interests.skeleton';

export const ProfileSkeleton = () => {
  return (
    <>
      <PhotoPreviewSkeleton />
      <NameSkeleton />
      <AboutProfileSkeleton />
      <InterestsSkeleton />
    </>
  );
};
