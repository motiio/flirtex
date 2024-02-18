import { Gender } from '../constants';

export interface FilterI {
  looking_gender: Gender;
  age_from: number;
  age_to: number;
  max_distance: number;
}
