import { MouseEvent, ReactNode, useState } from 'react';
import { Placement as PopperPlacementT } from '@popperjs/core';
import { usePopper } from 'react-popper';
import cn from 'classnames';
import styles from './Dropdown.module.scss';

interface DropdownProps {
  children: [ReactNode, ReactNode];
  placement?: PopperPlacementT;
  canClose?: boolean;
  isModal?: boolean;
  className?: string;
  buttonClassName?: string;
  dropdownClassName?: string;
}

export const Dropdown = ({
  children,
  placement = 'auto',
  canClose = false,
  isModal = true,
  className,
  buttonClassName,
  dropdownClassName,
}: DropdownProps) => {
  const [referenceElement, setReferenceElement] = useState<HTMLButtonElement | null>(null);
  const [popperElement, setPopperElement] = useState<HTMLDivElement | null>(null);
  const [isOpen, setIsOpen] = useState(false);

  const { styles: popperStyles, attributes } = usePopper(referenceElement, popperElement, {
    placement,
  });

  const clickButtonHandler = (e: MouseEvent<HTMLButtonElement>) => {
    e.stopPropagation();
    setIsOpen(!isOpen);
  };

  const closeHandler = (e: MouseEvent<HTMLDivElement>) => {
    e.stopPropagation();

    if (canClose) {
      setIsOpen(false);
    }
  };

  return (
    <div className={cn(styles.dropdownContainer, className)}>
      <button
        type="button"
        className={cn(styles.trigger, buttonClassName)}
        onClick={clickButtonHandler}
        ref={setReferenceElement}
      >
        {children[0]}
      </button>
      {isOpen && (
        <>
          <div
            className={cn(styles.dropdown, dropdownClassName)}
            ref={setPopperElement}
            style={popperStyles.popper}
            {...attributes.popper}
            onClick={closeHandler}
            role="presentation"
          >
            {children[1]}
          </div>
          {isModal && <div className={styles.modalWrapper} onClick={closeHandler} role="presentation" />}
        </>
      )}
    </div>
  );
};
