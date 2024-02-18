import RcSlider, { SliderProps } from 'rc-slider';
import 'rc-slider/assets/index.css';

export const Slider = (props: SliderProps) => {
  return (
    <RcSlider
      {...props}
      styles={{
        track: { backgroundColor: 'var(--tg-theme-button-color)' },
        rail: { backgroundColor: 'var(--tg-theme-button-disabled-color)' },
        handle: {
          borderColor: 'var(--tg-theme-button-color)',
          backgroundColor: 'var(--tg-theme-button-color)',
          opacity: 1,
        },
      }}
    />
  );
};
