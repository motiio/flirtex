import styles from './ProfileSkeleton.module.scss';
import { PhotoPreviewSkeleton } from '../PhotoPreview/PhotoPreview.skeleton';
import { NameSkeleton } from '../Name/Name.skeleton';
import { AboutProfileSkeleton } from '../AboutProfile/AboutProfile.skeleton';
import { InterestsSkeleton } from '../Interests/Interests.skeleton';

export const ProfileSkeleton = () => {
  return (
    <div className={styles.profileSkeletonContainer}>
      <PhotoPreviewSkeleton />
      <NameSkeleton />
      <AboutProfileSkeleton />
      <InterestsSkeleton />
    </div>
  );
};
