export interface IPatientTreatment {
  count: number;
  next: null;
  previous: null;
  results: Result[];
}

interface Result {
  id: number;
  patient: Patient;
  doctor: Patient;
  treatment: Treatment;
  treatment_date: string;
  description: string;
  follow_up_date: string;
}

interface Treatment {
  id: number;
  name: string;
  description: string;
}

interface Patient {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}

export interface IDoctorTreatment {
  count: number;
  next: null;
  previous: null;
  results: DResult[];
}

interface DResult {
  id: number;
  patient: DPatient;
  doctor: DPatient;
  treatment: DTreatment;
  treatment_date: string;
  description: string;
  follow_up_date: string;
}

interface DTreatment {
  id: number;
  name: string;
  description: string;
}

interface DPatient {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}
