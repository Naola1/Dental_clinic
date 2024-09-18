import { Description } from "@radix-ui/react-toast";

export interface ILogin {
  email: string;
  password: string;
}

export interface IForgotPassword {
  email: string;
}

export interface IResetPassword {
  token: string;
  password: string;
}

export interface IRegister {
  email: string;
  username: string;
  password: string;
}

export interface LoginResponse {
  message: string;
  user_id: number;
  email: string;
  role: string;
  access_token: string;
}

export interface ForgotPasswordRes {
  status: string;
}
export interface SidebarItem {
  title: string;
  href: string;
}

export interface IProfileUpdate {
  user: User;
  medical_history: string;
  allergies: string;
}

interface User {
  username: string;
  email: string;
  first_name: string;
  middle_name: string;
  last_name: string;
  gender: string;
  date_of_birth: string;
  phone_number: string;
  address: string;
  emergency_contact_name: string;
  emergency_contact_number: string;
  role: string;
}

interface ITreatmentRes {
  count: number;
  next: null;
  previous: null;
  results: IResult[];
}

interface IResult {
  id: number;
  name: string;
  description: string;
}
