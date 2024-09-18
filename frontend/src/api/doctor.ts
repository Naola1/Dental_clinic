import {
  BookingProps,
  IAppointmentStatus,
  IBookingResponse,
  IDoctorResponse,
  IDoctorsAvailablitySingle,
  ISingleDoctor,
} from "../../types/doctor";
import axiosInstance from "./axios";

export const getAllDoctors = async (): Promise<IDoctorResponse> => {
  const response = await axiosInstance.get("/doctors");
  return response.data;
};

export const getSingleDoctor = async (id: number): Promise<ISingleDoctor> => {
  const response = await axiosInstance.get(`/doctors/${id}`);
  return response.data;
};

export const booking = async ({
  id,
  data,
}: BookingProps): Promise<IBookingResponse> => {
  const response = await axiosInstance.post(
    `/bookings/${id}/book_appointment/`,
    {
      appointment_date: data.appointment_date,
    }
  );
  return response.data;
};

export const getSingleDoctorAvailablity = async (
  id: number
): Promise<IDoctorsAvailablitySingle[]> => {
  const response = await axiosInstance.get(`/doctors/${id}/availability`);
  return response.data;
};

export const changeAppointmentStatus = async ({
  id,
  data,
}: IAppointmentStatus) => {
  const response = await axiosInstance.put(
    `/appointments/${id}/change_status/`,
    {
      status: data.status,
    }
  );
  return response.data;
};
