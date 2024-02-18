import { ChangeEvent, KeyboardEvent, useState } from 'react';
import { useLoginUserAuthPostMutation } from '../../../../redux/api/cheerApi';
import styles from './WithoutTelegram.module.scss';

export const WithoutTelegram = () => {
  const [inputValue, setInputValue] = useState('FlirtexBot');
  const [firstAuth, { isLoading: authIsLoading, isError }] = useLoginUserAuthPostMutation();

  const changeHandler = (e: ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  const keyDownHandler = async (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      await firstAuth({
        userAgent: 'USER_TOKEN',
        userLoginRequest: { initData: inputValue },
      });
    }
  };

  return (
    <div className={styles.wrapper}>
      <div className={styles.title}>Вы что то сделали не так...</div>
      <div> Попробуйте зайти к нам в телеграм</div>
      <input type="text" value={inputValue} onChange={changeHandler} onKeyDown={keyDownHandler} />
    </div>
  );
};
