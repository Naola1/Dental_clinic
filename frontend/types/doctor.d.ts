import { BookingSchema } from "@/schema/doctors";

export interface IDoctorResponse {
  count: number;
  next: null;
  previous: null;
  results: Result[];
}

interface Result {
  id: number;
  user: User;
  specialization: string;
  bio: string;
  profile_picture: null;
  experience: number;
  qualification: string;
}

export interface User {
  username: string;
  email: string;
  first_name: string;
  middle_name: string;
  last_name: string;
  gender: string;
  date_of_birth: null;
  phone_number: string;
  address: string;
  emergency_contact_name: string;
  emergency_contact_number: string;
  role: string;
}

export interface ISingleDoctor {
  user: IUser;
  specialization: string;
  bio: string;
  profile_picture: null;
  experience: number;
  qualification: string;
}

interface IUser {
  username: string;
  email: string;
  first_name: string;
  middle_name: string;
  last_name: string;
  gender: string;
  date_of_birth: null;
  phone_number: string;
  address: string;
  emergency_contact_name: string;
  emergency_contact_number: string;
  role: string;
}

export interface IBooking {
  appointment_date: string;
}

export interface IBookingResponse {
  id: string;
  patient: string;
  doctor: string;
  appointment_date: string;
  status: string;
}

export interface BookingProps {
  id: number;
  data: {
    appointment_date: string;
  };
}

export interface IAppointmentStatus {
  id: number;
  data: {
    status: string;
  };
}

interface IDoctorsAvailablity {
  count: number;
  next: null;
  previous: null;
  results: DoctorsAvailablity[];
}

interface IDoctorsAvailablitySingle {
  id: number;
  doctor: number;
  day_of_week: string;
}
