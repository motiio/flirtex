export const generateLocalPhoto = async (photo: File) => {
  const reader = new FileReader();
  const promise = new Promise<string>((resolve) => {
    reader.onload = () => {
      resolve(reader.result as string);
    };
  });
  reader.readAsDataURL(photo);
  return promise;
};
