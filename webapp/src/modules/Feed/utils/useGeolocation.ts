import { useEffect, useState } from 'react';
import { LocationI } from '../../../utils/interfaces';

interface useGeoLocationOutput {
  update: VoidFunction;
  location: LocationI | null;
  isLoading: boolean;
  error: string;
  isSuccess: boolean;
}

export const useGeolocation = (): useGeoLocationOutput => {
  const [location, setLocation] = useState<LocationI | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [isSuccess, setIsSuccess] = useState(false);

  useEffect(() => {
    let timeout: NodeJS.Timeout;

    if (isLoading) {
      timeout = setTimeout(() => {
        setIsLoading(false);
        setError('Включите геолокацию на устройстве и повторите');
      }, 5000);
    }

    return () => clearTimeout(timeout);
  }, [isLoading]);

  const update = () => {
    if ('geolocation' in navigator) {
      setError('');
      setIsLoading(true);
      setIsSuccess(false);
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setLocation({ longitude: position.coords.longitude, latitude: position.coords.latitude });
          setError('');
          setIsLoading(false);
          setIsSuccess(true);
        },
        (positionError) => {
          setError(
            positionError.message === 'User denied Geolocation'
              ? 'Пользователь отказал в предоставлении геопозиции'
              : positionError.message,
          );
          setIsLoading(false);
        },
      );
    }
  };

  return { update, location, isLoading, isSuccess, error };
};
