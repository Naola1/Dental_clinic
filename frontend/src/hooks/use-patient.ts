import {
  getDoctorDashboardAppointment,
  getPatientDashboardAppointment,
  searchAppointment,
  searchRecord,
} from "@/api/patient";
import { useQuery } from "@tanstack/react-query";

export const usePADashboard = () => {
  return useQuery({
    queryKey: ["getPatientDashboardAppointment"],
    queryFn: getPatientDashboardAppointment,
  });
};

export const useDADashboard = (page_size?: string) => {
  return useQuery({
    queryKey: ["DADashboard", page_size],
    queryFn: () =>
      getDoctorDashboardAppointment({ page_size: page_size ?? "3" }),
  });
};

export const useSearchAppointment = (q?: string) => {
  return useQuery({
    queryKey: ["search-appointment", q],
    queryFn: () => searchAppointment({ q }),
  });
};

export const useSearchRecord = (q?: string) => {
  return useQuery({
    queryKey: ["search-record", q],
    queryFn: () => searchRecord({ q }),
  });
};
