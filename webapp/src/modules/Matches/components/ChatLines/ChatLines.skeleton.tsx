import styles from './ChatLines.module.scss';
import { generateId } from '../../../../utils/handlers/generateId';
import { ChatLineSkeleton } from '../ChatLine/ChatLine.skeleton';

export const ChatLinesSkeleton = () => {
  return (
    <div className={styles.chatLineContainer}>
      {Array.from(Array(10)).map(() => (
        <ChatLineSkeleton key={generateId()} />
      ))}
    </div>
  );
};
