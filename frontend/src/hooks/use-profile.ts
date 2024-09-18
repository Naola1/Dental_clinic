import { getPatientProfile } from "@/api/profile";
import { useQuery } from "@tanstack/react-query";

export const usePatientProfile = () => {
  return useQuery({
    queryKey: ["patient-profile"],
    queryFn: getPatientProfile,
  });
};
