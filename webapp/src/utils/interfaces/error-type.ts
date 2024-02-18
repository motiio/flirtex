import { SerializedError } from '@reduxjs/toolkit';
import { CustomErrorI } from './api-error';

export type ErrorT = CustomErrorI | SerializedError | string;
