import styles from './AboutProfile.module.scss';

interface AboutProfileProps {
  info: string;
}

export const AboutProfile = ({ info }: AboutProfileProps) => {
  return (
    <div className={styles.aboutProfileContainer}>
      <div className={styles.block}>
        <div className={styles.title}>Обо мне</div>
        <div>
          <p>{info}</p>
        </div>
      </div>
    </div>
  );
};
