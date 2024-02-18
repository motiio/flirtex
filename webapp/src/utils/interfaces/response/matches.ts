import { PaginationI } from '../pagination';

export interface MatchesProfileI {
  bio: string | null;
  match_id: string;
  name: string;
  photo_url: string;
  profile_id: string;
  tg_username: string;
}

export interface MatchesResponseI {
  pagination: PaginationI;
  profiles: MatchesProfileI[];
}
