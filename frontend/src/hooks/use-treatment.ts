import { getDoctorTreatment, getPatientTreatment } from "@/api/treatment";
import { useQuery } from "@tanstack/react-query";

export const useTreatment = () => {
  return useQuery({
    queryKey: ["patient-treatment"],
    queryFn: getPatientTreatment,
  });
};

export const useDoctorTreatment = () => {
  return useQuery({
    queryKey: ["doctor-treatment"],
    queryFn: getDoctorTreatment,
  });
};
