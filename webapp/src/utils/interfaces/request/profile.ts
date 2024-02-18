import { Gender } from '../../constants';
import { LocationI } from '../location';

export interface ProfileRequestI {
  name: string;
  birthdate: string;
  gender: Gender;
  looking_gender?: Gender;
  location?: LocationI;
}

export interface ProfileUpdateRequestI {
  bio?: string;
  location?: LocationI;
  interests?: string[];
}
