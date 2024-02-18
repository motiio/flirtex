import { Gender } from '../../constants';
import { InterestI } from '../interest';
import { PhotoI } from '../photo';

export interface ProfileResponseI {
  id: string;
  name: string;
  looking_gender: Gender;
  gender: Gender;
  photos: PhotoI[];
  interests: InterestI[];
  bio: string | null;
  age: number;
  has_location: boolean;
  distance: number;
}
