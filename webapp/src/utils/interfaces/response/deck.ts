import { ProfileResponseI } from './profile';

export interface BatchI extends ProfileResponseI {
  distance: number;
}

export interface DeckResponseI {
  batch: BatchI[];
}
