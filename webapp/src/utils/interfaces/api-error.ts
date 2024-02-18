export interface CustomErrorI {
  status: number;
  data: { detail: { msg: string } | { msg: string }[] };
  error: string;
}
