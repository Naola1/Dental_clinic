import {
  booking,
  changeAppointmentStatus,
  getAllDoctors,
  getSingleDoctor,
  getSingleDoctorAvailablity,
} from "@/api/doctor";
import { getTreatments } from "@/api/profile";
import { useMutation, useQuery } from "@tanstack/react-query";
import { BookingProps, IAppointmentStatus } from "types/doctor";

export const useAllDoctors = () => {
  return useQuery({
    queryKey: ["allDotors"],
    queryFn: getAllDoctors,
  });
};

export const useSingleDoctors = (id: number) => {
  return useQuery({
    queryKey: ["singleDoctor", id],
    queryFn: () => getSingleDoctor(id),
  });
};

export const useBooking = () => {
  return useMutation({
    mutationFn: ({ id, data }: BookingProps) => booking({ id, data }),
  });
};

export const usePDA = (id: number) => {
  return useQuery({
    queryKey: ["pda"],
    queryFn: () => getSingleDoctorAvailablity(id),
  });
};

export const useChangeStatus = () => {
  return useMutation({
    mutationFn: ({ id, data }: IAppointmentStatus) =>
      changeAppointmentStatus({ id, data }),
  });
};

export const useGetTreatments = () => {
  return useQuery({
    queryKey: ["treatments"],
    queryFn: getTreatments,
  });
};
