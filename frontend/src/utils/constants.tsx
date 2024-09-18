import { SidebarItem } from "types/auth";

export const PatientSidebar: SidebarItem[] = [
  {
    title: "Dashboard",
    href: "/patient/dashboard",
  },
  {
    title: "Doctors",
    href: "/patient/doctors",
  },
  {
    title: "Treatment",
    href: "/patient/treatment",
  },

  {
    title: "Profile",
    href: "/patient/profile",
  },
];

export const DoctorSidebar: SidebarItem[] = [
  {
    title: "Dashboard",
    href: "/doctor/dashboard",
  },
  {
    title: "Doctors",
    href: "/doctor/doctors",
  },
  {
    title: "Patient-Records",
    href: "/doctor/patient-records",
  },
  {
    title: "Appointment",
    href: "/doctor/appointment",
  },
  {
    title: "Profile",
    href: "/doctor/profile",
  },
];

export const ReceptionistSidebar: SidebarItem[] = [
  {
    title: "Dashboard",
    href: "/receptionist/dashboard",
  },
  {
    title: "Doctors",
    href: "/receptionist/doctors",
  },

  {
    title: "Appointment",
    href: "/receptionist/appointment",
  },
  {
    title: "Profile",
    href: "/receptionist/profile",
  },
];
