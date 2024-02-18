import { Gender } from '../../constants';
import { PhotoI } from '../photo';
import { PaginationI } from '../pagination';

export interface LikeReactionsProfileI {
  age: number;
  gender: Gender;
  id: string;
  name: string;
  photos: PhotoI[];
}

export interface LikeReactionsResponseI {
  pagination: PaginationI;
  profiles: LikeReactionsProfileI[];
}
