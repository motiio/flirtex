export const generateId = () => {
  return (~~(Math.random() * 1e8)).toString(16);
};
