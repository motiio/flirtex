export const cropText = (text: string, maxLength = 60) => {
  if (!text) {
    return '';
  }

  const trimmed = text.substring(0, maxLength);
  let step = 1;

  while (trimmed[trimmed.length - step] !== ' ' && trimmed.length <= step) {
    step++;
  }

  const cutText = trimmed.substring(0, maxLength - step);
  return cutText[cutText.length - 1] === '.' ? `${cutText}..` : `${cutText}...`;
};
