export interface IPAppointmentDashboard {
  count: number;
  next: string;
  previous: null;
  results: Result[];
}

interface Result {
  id: number;
  patient: number;
  doctor: Doctor;
  appointment_date: string;
  status: string;
}

interface Doctor {
  id: number;
  user: User;
  specialization: string;
}

interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  middle_name: string;
  last_name: string;
  role: string;
}

export interface IDoctorAppointmentDashboard {
  count: number;
  next: null;
  previous: null;
  results: DResult[];
}

interface DResult {
  id: number;
  patient: DPatient;
  doctor: DDoctor;
  appointment_date: string;
  status: string;
}

interface DDoctor {
  id: number;
  user: DUser;
  specialization: string;
}

interface DPatient {
  id: number;
  user: DUser;
}

interface DUser {
  id: number;
  username: string;
  email: string;
  first_name: string;
  middle_name: string;
  last_name: string;
  role: string;
}

export interface ISearch {
  id: number;
  patient: SPatient;
  doctor: SDoctor;
  appointment_date: string;
  status: string;
}

interface SDoctor {
  id: number;
  user: SUser;
  specialization: string;
}

interface SPatient {
  id: number;
  user: User;
}

interface SUser {
  id: number;
  username: string;
  email: string;
  first_name: string;
  middle_name: string;
  last_name: string;
  role: string;
}

export interface ISearchRecord {
  id: number;
  patient: RPatient;
  doctor: RPatient;
  treatment: RTreatment;
  treatment_date: string;
  description?: string;
  follow_up_date: null;
}

interface RTreatment {
  id: number;
  name: string;
  description: string;
}

interface RPatient {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}
