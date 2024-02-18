import { ChangeEvent } from 'react';
import WebApp from '@twa-dev/sdk';
import { MAX_FILE_SIZE } from '../constants';

export function loadPhoto(e: ChangeEvent<HTMLInputElement>, isFileFormat: true): File | undefined;

export function loadPhoto(e: ChangeEvent<HTMLInputElement>, isFileFormat: false): FormData | undefined;

export function loadPhoto(e: ChangeEvent<HTMLInputElement>, isFileFormat: boolean): File | FormData | undefined {
  if (!e.target.files) {
    return;
  }

  const file = e.target.files[0];

  if (file.size > MAX_FILE_SIZE) {
    WebApp.showAlert('Файл слишком большой! Выберите файл, который не превышает 5 МБ.');
    return;
  }

  if (file.type !== 'image/jpeg' && file.type !== 'image/jpg') {
    WebApp.showAlert('Неверный формат файла. Ожидается jpeg/jpg');
    return;
  }

  if (isFileFormat) {
    return file;
  }

  const photoList = new FormData();
  photoList.append('photo', file);
  return photoList;
}
