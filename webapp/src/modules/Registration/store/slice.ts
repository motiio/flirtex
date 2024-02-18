import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { Gender } from '../../../utils/constants';

interface RegistrationDataI {
  name: string;
  day: string;
  month: string;
  year: string;
  gender: Gender;
}

interface ErrorsI {
  name: boolean;
  day: boolean;
  month: boolean;
  year: boolean;
  gender: boolean;
}

interface RegistrationStateI {
  formData: RegistrationDataI;
  hasErrors: ErrorsI;
}

const initialState: RegistrationStateI = {
  formData: { name: '', day: '', month: '', year: '', gender: Gender.other },
  hasErrors: { name: true, day: true, month: true, year: true, gender: true },
};

const registrationSlice = createSlice({
  name: 'registration',
  initialState,
  reducers: {
    setFormData(state, action: PayloadAction<Partial<RegistrationDataI>>) {
      state.formData = { ...state.formData, ...action.payload };
    },
    reset(state) {
      state.formData = initialState.formData;
    },
    setHasErrors(state, action: PayloadAction<Partial<ErrorsI>>) {
      state.hasErrors = { ...state.hasErrors, ...action.payload };
    },
  },
});

export { registrationSlice };
