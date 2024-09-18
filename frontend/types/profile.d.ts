export interface IPatientProfile {
  user: User;
  medical_history?: string;
  allergies?: string;
  specialization?: string;
  bio?: string;
  profile_picture?: string;
  experience?: string;
  qualification?: string;
}

interface User {
  username: string;
  email: string;
  first_name: string;
  middle_name: string;
  last_name: string;
  gender: string;
  date_of_birth?: strng;
  phone_number: string;
  address: string;
  emergency_contact_name: string;
  emergency_contact_number: string;
  role: string;
}
