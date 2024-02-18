import { MainButton } from '@twa-dev/sdk/react';

interface TelegramButtonProps {
  text: string;
  onClick: VoidFunction;
  isDisabled?: boolean;
  isLoading?: boolean;
}

const styles = getComputedStyle(document.documentElement);
const buttonColor = styles.getPropertyValue('--tg-theme-button-color');
const buttonTextColor = styles.getPropertyValue('--tg-theme-button-text-color');
const buttonDisabledColor = styles.getPropertyValue('--tg-theme-button-disabled-color');
const buttonDisabledTextColor = styles.getPropertyValue('--tg-theme-button-disabled-text-color');

export const TelegramButton = ({ text, onClick, isDisabled, isLoading }: TelegramButtonProps) => {
  const color = isDisabled || isLoading ? buttonDisabledColor : buttonColor;
  const textColor = isDisabled || isLoading ? buttonDisabledTextColor : buttonTextColor;

  return (
    <MainButton
      text={text}
      onClick={onClick}
      disabled={isDisabled}
      progress={isLoading}
      color={color}
      textColor={textColor}
    />
  );
};
